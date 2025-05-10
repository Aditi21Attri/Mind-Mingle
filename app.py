from flask import Flask, render_template, redirect, url_for, jsonify, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Email, Length, EqualTo, ValidationError
from models import db, User, Mood, SavedQuote, BlogPost
from dbm import sqlite3
import requests
from meditation import get_random_meditation
from models import Comment

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
@app.route('/mood', methods=['GET', 'POST'])
@login_required
def mood():
    if request.method == 'POST':
        mood = request.form['mood']
        text = mood
        results = classifier(text)
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
        if content:
            post = BlogPost(content=content, user_id=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash('Your story has been shared anonymously!', 'success')
            return redirect(url_for('blog'))

    posts = BlogPost.query.order_by(BlogPost.timestamp.desc()).all()
    return render_template('blog.html', posts=posts)


@app.route('/blog/<int:post_id>/comment', methods=['POST'])
@login_required
def comment(post_id):
    content = request.form.get('comment')
    if content:
        new_comment = Comment(content=content, blog_id=post_id, user_id=current_user.id)
        db.session.add(new_comment)
        db.session.commit()
    return redirect(url_for('blog'))


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