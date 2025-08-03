from flask import Flask, render_template, redirect, url_for, jsonify, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Email, Length, EqualTo, ValidationError
from models import db, User, Mood, SavedQuote, BlogPost
from models import Comment, blog_likes
from dbm import sqlite3
import requests
from meditation import get_random_meditation

#MODEL
from transformers import pipeline

# Load model
classifier = pipeline(
    "text-classification",
    model='bhadresh-savani/distilbert-base-uncased-emotion',
    return_all_scores=True
)


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/moodmingle'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///moodmingle.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=80)])
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(username=username.data).first()
        if existing_user_username:
            raise ValidationError('Username already exists. Please choose a different one.')

    def validate_email(self, email):
        existing_user_email = User.query.filter_by(email=email.data).first()
        if existing_user_email:
            raise ValidationError('Email already exists. Please choose a different one.')


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('home'))
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, email=form.email.data)
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))
from flask import request, flash

def fetch_random_quote():
    url = "https://zenquotes.io/api/random"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and len(data) > 0:
                quote = data[0].get('q')
                author = data[0].get('a')
                return f"{quote} — {author}"
    except Exception as e:
        print("Quote fetch error:", e)
    return "Stay motivated and keep going!"
@app.route('/quote', methods=['GET'])
@login_required
def get_quote():
    quote = fetch_random_quote()
    return jsonify({'quote': quote})
@app.route('/save_quote', methods=['POST'])
@login_required
def save_quote():
    quote = request.form['quote']
    saved = SavedQuote(quote=quote, user_id=current_user.id)
    db.session.add(saved)
    db.session.commit()
    return jsonify({'status': 'saved'})
@app.route('/saved_quotes')
@login_required
def saved_quotes():
    quotes = SavedQuote.query.filter_by(user_id=current_user.id).all()
    return jsonify([q.quote for q in quotes])
@app.route('/mood-history')
def mood_history():
    username = session.get('username')
    page = int(request.args.get('page', 1))
    per_page = 10
    offset = (page - 1) * per_page
    conn = sqlite3.connect('mood.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT mood, note, timestamp
        FROM mood_entries
        WHERE username = ?
        ORDER BY timestamp DESC
        LIMIT ? OFFSET ?
    ''', (username, per_page, offset))
    entries = cursor.fetchall()
    # Count total for pagination
    cursor.execute('''
        SELECT COUNT(*)
        FROM mood_entries
        WHERE username = ?
    ''', (username,))
    total = cursor.fetchone()[0]
    conn.close()
    total_pages = (total + per_page - 1) // per_page
    return render_template(
        'mood.html',
        entries=entries,
        page=page,
        total_pages=total_pages
    )

# def analyze_sentiment(text):
#     text = text.lower()
#     if any(word in text for word in ['sad', 'depressed', 'unhappy']):
#         return 'negative'
#     elif any(word in text for word in ['happy', 'joyful', 'excited']):
#         return 'positive'
#     elif any(word in text for word in ['angry', 'frustrated', 'irritated']):
#         return 'angry'
#     elif any(word in text for word in ['anxious', 'nervous', 'worried']):
#         return 'anxious'
#     else:
#         return 'neutral'
@app.route('/delete_mood/<int:mood_id>', methods=['POST'])
@login_required
def delete_mood(mood_id):
    mood = Mood.query.get_or_404(mood_id)
    if mood.user_id != current_user.id:
        flash('Unauthorized action!', 'danger')
        return redirect(url_for('mood'))

    db.session.delete(mood)
    db.session.commit()
    flash('Mood entry deleted successfully!', 'success')
    return redirect(url_for('mood'))
emotion_to_mood = {
    'joy': 'happy',
    'love': 'happy',
    'gratitude': 'happy',
    'hope': 'happy',
    'compassion': 'happy',
    'pride': 'happy',
    'amusement': 'happy',
    'excitement': 'happy',
    'relief': 'happy',
    'trust': 'happy',

    'sadness': 'sad',
    'grief': 'sad',
    'loneliness': 'sad',
    'melancholy': 'sad',
    'guilt': 'sad',
    'shame': 'sad',
    'disappointment': 'sad',

    'anger': 'angry',
    'rage': 'angry',
    'irritation': 'angry',
    'frustration': 'angry',
    'resentment': 'angry',

    'fear': 'anxious',
    'nervousness': 'anxious',
    'worry': 'anxious',
    'panic': 'anxious',
    'insecurity': 'anxious',
    'jealousy': 'anxious',
    'envy': 'anxious',

    'confusion': 'neutral',
    'curiosity': 'neutral',
    'surprise': 'neutral',
    'boredom': 'neutral',
    'contentment': 'neutral',
    'awe': 'neutral',
    'embarrassment': 'neutral',

    'stress': 'stressed',
    'overwhelm': 'stressed',
    'burnout': 'stressed',
    'anxiety': 'stressed'
}

def preprocess_text_for_emotion(text):
    """Preprocess text to handle negations and improve emotion detection"""
    text_lower = text.lower().strip()
    
    # Handle explicit negations - if someone says "not happy", they're likely sad
    negation_patterns = {
        'not happy': 'sad and unhappy',
        'not feeling well': 'unwell and sad',
        'not good': 'bad and sad',
        'not okay': 'sad and troubled',
        'not fine': 'sad and troubled',
        'not great': 'sad and disappointed',
        'not excited': 'disappointed and sad',
        'not feeling good': 'unwell and sad',
        "i'm not": 'I am feeling sad and',
        "im not": 'I am feeling sad and',
        "i am not": 'I am feeling sad and',
        "don't feel": 'I feel sad and',
        "dont feel": 'I feel sad and',
        "can't": 'unable and frustrated',
        "cant": 'unable and frustrated',
        "won't": 'unwilling and frustrated',
        "wont": 'unwilling and frustrated'
    }
    
    # Apply negation transformations
    for pattern, replacement in negation_patterns.items():
        if pattern in text_lower:
            text_lower = text_lower.replace(pattern, replacement)
    
    # Handle general negation words that flip meaning
    negative_indicators = ['not', 'no', 'never', 'nothing', 'nowhere', 'neither', 'none']
    positive_words = ['happy', 'good', 'great', 'excellent', 'wonderful', 'amazing', 'fantastic', 'awesome']
    
    words = text_lower.split()
    processed_words = []
    
    i = 0
    while i < len(words):
        word = words[i]
        # Check if current word is a negation followed by a positive word
        if word in negative_indicators and i + 1 < len(words):
            next_word = words[i + 1]
            if any(pos_word in next_word for pos_word in positive_words):
                # Replace "not good" type patterns with sad indicators
                processed_words.extend(['sad', 'unhappy', 'troubled'])
                i += 2  # Skip the next word since we processed it
                continue
        
        processed_words.append(word)
        i += 1
    
    return ' '.join(processed_words)

@app.route('/mood', methods=['GET', 'POST'])
@login_required
def mood():
    if request.method == 'POST':
        mood = request.form['mood']
        
        # Preprocess text to handle negations
        processed_text = preprocess_text_for_emotion(mood)
        print(f"Original text: {mood}")
        print(f"Processed text: {processed_text}")
        
        results = classifier(processed_text)
        top_emotion = max(results[0], key=lambda x: x['score'])['label']
        print("Detected Emotion:", top_emotion)
        mood_cal = emotion_to_mood.get(top_emotion, 'neutral')
        print("Mapped Mood:", mood_cal)
        note = request.form.get('note', '')
        new_mood = Mood(mood=mood_cal, note=note, user_id=current_user.id)
        db.session.add(new_mood)
        db.session.commit()
        # recommendation = get_random_meditation(mood)
        flash('Mood submitted successfully!', 'success')

    moods = Mood.query.filter_by(user_id=current_user.id).order_by(Mood.timestamp.asc()).all()
    # Pagination setup
    page = request.args.get('page', 1, type=int)
    per_page = 5

    moods_paginated = Mood.query.filter_by(user_id=current_user.id) \
        .order_by(Mood.timestamp.desc()) \
        .paginate(page=page, per_page=per_page)
    all_moods = Mood.query.filter_by(user_id=current_user.id).order_by(Mood.timestamp.asc()).all()
    # Prepare data for mood graph
    mood_labels = [m.timestamp.strftime("%b %d") for m in moods]
    mood_values = [m.mood.lower() for m in moods]

    # Convert moods to numeric values for charting
    mood_mapping = {
        "happy": 5,
        "excited": 4,
        "neutral": 3,
        "anxious": 2,
        "sad": 1,
        "angry": 1,
        "depressed": 1
    }
    mood_scores = [mood_mapping.get(m, 3) for m in mood_values]  # Default to 3 (neutral)

    recommendation = get_random_meditation(moods[-1].mood) if moods else ""

    return render_template('mood.html',
                           moods=moods_paginated,
                           recommendation=recommendation,
                           mood_labels=mood_labels,
                           mood_scores=mood_scores)

@app.route('/blog', methods=['GET', 'POST'])
@login_required
def blog():
    if request.method == 'POST':
        content = request.form.get('content')
        mood = request.form.get('mood')
        
        if content and len(content.strip()) >= 10:
            # Basic crisis detection
            crisis_keywords = ['suicide', 'kill myself', 'end it all', 'not worth living', 'hurt myself']
            content_lower = content.lower()
            has_crisis_content = any(keyword in content_lower for keyword in crisis_keywords)
            
            if has_crisis_content:
                flash('We noticed you might be going through a difficult time. Please consider reaching out for support. Your safety matters.', 'warning')
                # Still allow the post but add a note
                content += "\n\n[Note: If you're struggling, please reach out to crisis support: 988 (Suicide Prevention Lifeline)]"
            
            post = BlogPost(
                content=content, 
                mood=mood if mood else 'neutral',
                user_id=current_user.id
            )
            db.session.add(post)
            db.session.commit()
            flash('Your story has been shared anonymously!', 'success')
            return redirect(url_for('blog'))
        else:
            flash('Please write at least 10 characters to share your story.', 'error')

    posts = BlogPost.query.order_by(BlogPost.timestamp.desc()).all()
    
    # Calculate some stats for the template
    total_comments = db.session.query(db.func.count(Comment.id)).scalar()
    total_users = db.session.query(db.func.count(User.id)).scalar()
    
    return render_template('blog.html', 
                         posts=posts, 
                         total_comments=total_comments,
                         total_users=total_users)


@app.route('/blog/<int:post_id>/like', methods=['POST'])
@login_required
def like_post(post_id):
    """Toggle like for a blog post"""
    post = BlogPost.query.get_or_404(post_id)
    
    if current_user in post.liked_by:
        # Unlike the post
        post.liked_by.remove(current_user)
        post.likes = max(0, post.likes - 1)
        liked = False
    else:
        # Like the post
        post.liked_by.append(current_user)
        post.likes += 1
        liked = True
    
    db.session.commit()
    
    if request.is_json:
        return jsonify({
            'success': True, 
            'liked': liked, 
            'like_count': post.likes
        })
    
    return redirect(url_for('blog'))


@app.route('/blog/<int:post_id>/comment', methods=['POST'])
@login_required
def comment(post_id):
    content = request.form.get('comment')
    if content and len(content.strip()) >= 1:
        new_comment = Comment(content=content, blog_id=post_id, user_id=current_user.id)
        db.session.add(new_comment)
        db.session.commit()
        flash('Your comment has been added!', 'success')
    return redirect(url_for('blog'))


@app.route('/blog/filter/<mood>')
@login_required
def filter_blog_by_mood(mood):
    """Filter blog posts by mood"""
    if mood == 'all':
        posts = BlogPost.query.order_by(BlogPost.timestamp.desc()).all()
    else:
        posts = BlogPost.query.filter_by(mood=mood).order_by(BlogPost.timestamp.desc()).all()
    
    total_comments = db.session.query(db.func.count(Comment.id)).scalar()
    total_users = db.session.query(db.func.count(User.id)).scalar()
    
    return render_template('blog.html', 
                         posts=posts, 
                         total_comments=total_comments,
                         total_users=total_users,
                         current_filter=mood)

@app.route('/ai_chat', methods=['GET', 'POST'])
@login_required
def ai_chat():
    """AI Chat interface for users to talk with the AI"""
    from wtforms import TextAreaField, SubmitField
    from wtforms.validators import InputRequired, Length
    
    class ChatForm(FlaskForm):
        message = TextAreaField('Message', validators=[InputRequired(), Length(min=1, max=500)])
        submit = SubmitField('Send')
    
    form = ChatForm()
    conversation = session.get('conversation', [])
    
    if form.validate_on_submit():
        user_message = form.message.data
        
        # Get user's recent mood for context
        recent_mood = Mood.query.filter_by(user_id=current_user.id) \
                                .order_by(Mood.timestamp.desc()).first()
        
        mood_context = recent_mood.mood if recent_mood else None
        
        # Generate AI response using the same system as mood submission
        processed_text = preprocess_text_for_emotion(user_message)
        
        # Simple AI response generation
        ai_response = generate_simple_ai_response(user_message, mood_context)
        
        # Add to conversation
        conversation.append({
            'user': user_message,
            'ai': ai_response,
            'timestamp': request.form.get('timestamp', '')
        })
        
        # Keep only last 10 exchanges
        if len(conversation) > 10:
            conversation = conversation[-10:]
        
        session['conversation'] = conversation
        form.message.data = ''  # Clear the form
        
    return render_template('ai_chat.html', form=form, conversation=conversation)

def generate_simple_ai_response(user_input, mood=None):
    """Generate a simple AI response based on user input and mood context"""
    user_input_lower = user_input.lower()
    
    # Crisis detection keywords
    crisis_keywords = ['suicide', 'kill myself', 'end it all', 'worthless', 'hopeless']
    if any(keyword in user_input_lower for keyword in crisis_keywords):
        return """I'm very concerned about what you're sharing. Please reach out for immediate support:
        
🆘 National Suicide Prevention Lifeline: 988
📱 Crisis Text Line: Text HOME to 741741
🌐 International resources: iasp.info/resources/Crisis_Centres/

You matter, and there are people who want to help you through this difficult time."""

    # Context-aware responses based on mood and keywords
    if mood == 'sad' or any(word in user_input_lower for word in ['sad', 'depressed', 'down', 'crying']):
        return """I hear that you're going through a difficult time, and I want you to know that your feelings are completely valid. Sadness is a natural human emotion, and it's okay to feel this way.

Here are some gentle suggestions:
• Try the "Healing Light Visualization" meditation
• Reach out to someone you trust
• Practice self-compassion - treat yourself like you would a good friend
• Remember that feelings are temporary, even though they feel overwhelming right now

Would you like to talk more about what's contributing to these feelings?"""

    elif mood == 'anxious' or any(word in user_input_lower for word in ['anxious', 'worried', 'stressed', 'panic']):
        return """Anxiety can feel overwhelming, but you have the strength to work through this. Let's focus on grounding you in the present moment.

Try this right now:
• Take 3 deep breaths (4 seconds in, 6 seconds out)
• Name 5 things you can see around you
• Remember: anxiety is your mind trying to protect you, but you're safe right now

Some techniques that might help:
• Box breathing (4-4-4-4 pattern)
• Progressive muscle relaxation
• The 5-4-3-2-1 grounding technique

What triggered these anxious feelings today?"""

    elif mood == 'angry' or any(word in user_input_lower for word in ['angry', 'mad', 'frustrated', 'irritated']):
        return """I can sense your frustration, and anger is a valid emotion that often signals something important needs attention. Let's work with this energy constructively.

Immediate relief:
• Take 10 deep breaths, making your exhale longer than your inhale
• If possible, do some physical movement (walk, stretch, even punch a pillow safely)
• Try the "clenched fist release" technique

Questions to consider:
• What boundary was crossed that triggered this anger?
• What do you need to feel respected and heard?
• How can you channel this energy into positive action?

Anger often protects other feelings - what might be underneath it?"""

    elif mood == 'happy' or any(word in user_input_lower for word in ['happy', 'excited', 'great', 'awesome']):
        return """It's wonderful to hear positive energy from you! 🌟 I love that you're experiencing joy - these moments are so important to savor and appreciate.

Ways to amplify your happiness:
• Share this positive feeling with someone you care about
• Write down what's contributing to this joy
• Take a moment to really feel gratitude for this experience
• Consider doing something kind for someone else to spread the positivity

Your happiness is contagious! What's been the highlight of your day that's bringing you this joy?"""

    elif any(word in user_input_lower for word in ['thank', 'grateful', 'appreciate']):
        return """You're so welcome! It means a lot to me that you find our conversations helpful. Your gratitude actually brightens my day too.

Remember:
• You're doing important work by paying attention to your mental health
• Every small step toward wellness matters
• You have more strength than you realize

Is there anything specific you'd like to explore or talk about today?"""

    elif any(word in user_input_lower for word in ['help', 'advice', 'what should']):
        return """I'm here to support you, and I appreciate you reaching out. The fact that you're asking for help shows wisdom and courage.

To give you the best support, it would help to know:
• What's your current emotional state?
• What specific situation or feeling would you like help with?
• Have you tried any coping strategies recently?

Remember, you're the expert on your own life - I'm just here to offer gentle guidance and remind you of your own inner wisdom. What's on your mind today?"""

    else:
        return """Thank you for sharing with me. I'm here to listen and support you through whatever you're experiencing.

I notice you're reaching out, which shows self-awareness and courage. Whether you're having a good day or a challenging one, your feelings and experiences matter.

Some gentle questions to consider:
• How are you feeling right now, both emotionally and physically?
• What's one thing that went well for you today, even if it was small?
• Is there anything specific you'd like support with?

I'm here to listen without judgment and offer gentle guidance. What would be most helpful for you right now?"""

@app.route('/clear_chat')
@login_required
def clear_chat():
    """Clear the chat conversation"""
    session.pop('conversation', None)
    return redirect(url_for('ai_chat'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)





















#
# @app.route('/counselor-login', methods=['GET', 'POST'])
# def counselor_login():
#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['password']
#
#         counselor = Counselor.query.filter_by(email=email).first()
#         if counselor and check_password_hash(counselor.password, password):
#             session['user_type'] = 'counselor'
#             session['user_id'] = counselor.id
#             return redirect(url_for('counselor_dashboard'))
#         else:
#             flash('Invalid credentials!', 'danger')
#
#     return render_template('counselor_login.html')
# @app.route('/chat/<int:user_id>', methods=['GET', 'POST'])
# @login_required
# def chat(user_id):
#     # Only allow if current_user is user or counselor
#     if current_user.role not in ['user', 'counselor']:
#         abort(403)
#
#     other_user = User.query.get_or_404(user_id)
#
#     # Fetch chat history
#     chat = Message.query.filter(
#         ((Message.sender_id == current_user.id) & (Message.receiver_id == user_id)) |
#         ((Message.sender_id == user_id) & (Message.receiver_id == current_user.id))
#     ).order_by(Message.timestamp).all()
#
#     # Send message
#     if request.method == 'POST':
#         msg = Message(sender_id=current_user.id, receiver_id=user_id, message=request.form['message'])
#         db.session.add(msg)
#         db.session.commit()
#         return redirect(url_for('chat', user_id=user_id))
#
#     return render_template('chat.html', chat=chat, other_user=other_user)
#
# def get_recommendation(mood_text):
#     mood_text = mood_text.lower()
#     if "sad" in mood_text or "depressed" in mood_text:
#         return "Try a 5-minute breathing exercise or talk to a friend ❤️"
#     elif "happy" in mood_text or "excited" in mood_text:
#         return "Great! Maybe share your joy with someone 😄"
#     elif "angry" in mood_text:
#         return "Take a pause. Deep breaths. Try journaling it out 🧘"
#     elif "anxious" in mood_text or "nervous" in mood_text:
#         return "Ground yourself. Try the 5-4-3-2-1 sensory exercise 🧠"
#     else:
#         return "Stay mindful. Every emotion is valid 💬"

# def map_sentiment_to_exercise_type(sentiment):
#     mapping = {
#         'negative': 'stretching',
#         'positive': 'cardio',
#         'angry': 'strength',
#         'anxious': 'yoga',
#         'neutral': 'cardio'
#     }
#     return mapping.get(sentiment, 'cardio')


# def fetch_exercises(exercise_type):
#     api_url = 'https://api.api-ninjas.com/v1/exercises'
#     headers = {'X-Api-Key': 'sTL54qTIpWwUctwySOLJUQ==lVeOhBMhUz4NaLW4'}
#     params = {'type': exercise_type}
#     response = requests.get(api_url, headers=headers, params=params)
#     if response.status_code == 200:
#         return response.json()
#     else:
#         return []

# def fetch_random_quote():
    # url = "https://api.api-ninjas.com/v1/quotes"
    # headers = {'X-Api-Key': 'sTL54qTIpWwUctwySOLJUQ==lVeOhBMhUz4NaLW4'}
    # response = requests.get(url, headers=headers)
    # if response.status_code == 200:
    #     return response.json()[0]['quote']
    # return "Stay motivated and keep going!"