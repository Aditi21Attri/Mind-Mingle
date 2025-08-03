#!/usr/bin/env python3
"""
Demo script to showcase the enhanced blog features
"""

from app import app, db
from models import User, BlogPost, Comment
from werkzeug.security import generate_password_hash
import datetime

def create_demo_data():
    with app.app_context():
        # Create a demo user if not exists
        demo_user = User.query.filter_by(username='demo_user').first()
        if not demo_user:
            demo_user = User(
                username='demo_user',
                email='demo@example.com',
                password_hash=generate_password_hash('demo123')
            )
            db.session.add(demo_user)
            db.session.commit()
            print("✓ Created demo user")
        
        # Create sample blog posts with different moods
        sample_posts = [
            {
                'content': "Had an amazing day today! Started with a morning meditation and felt so centered. Then went for a hike and saw the most beautiful sunrise. Sometimes the simple moments bring the greatest joy. 🌅",
                'mood': 'happy'
            },
            {
                'content': "Feeling overwhelmed with work and life lately. It's like there's a weight on my chest that won't go away. But I know I'm not alone in this struggle, and reaching out helps.",
                'mood': 'anxious'
            },
            {
                'content': "Lost someone very close to me recently. The grief comes in waves - sometimes I'm okay, and sometimes I can barely breathe. Taking it one day at a time.",
                'mood': 'sad'
            },
            {
                'content': "Just got accepted into my dream program! I can't believe it's finally happening. All those late nights studying and working toward this goal have paid off. Dreams do come true! ✨",
                'mood': 'excited'
            },
            {
                'content': "Frustrated with how things are going at work. Feel like my ideas aren't being heard and my efforts aren't recognized. Need to find a way to address this constructively.",
                'mood': 'angry'
            },
            {
                'content': "Having a quiet day today. Not particularly happy or sad, just existing. Sometimes that's enough, and that's okay too.",
                'mood': 'neutral'
            }
        ]
        
        # Add sample posts
        for post_data in sample_posts:
            existing_post = BlogPost.query.filter_by(content=post_data['content']).first()
            if not existing_post:
                post = BlogPost(
                    content=post_data['content'],
                    mood=post_data['mood'],
                    user_id=demo_user.id,
                    likes=0
                )
                db.session.add(post)
        
        db.session.commit()
        print("✓ Created sample blog posts with different moods")
        
        # Add some sample comments
        posts = BlogPost.query.limit(3).all()
        sample_comments = [
            "Thank you for sharing this! It really resonates with me.",
            "Sending you love and support during this difficult time 💙",
            "Your strength is inspiring. Keep going!",
            "I'm going through something similar. We're in this together.",
            "Congratulations! You deserve all the success coming your way!"
        ]
        
        for i, post in enumerate(posts):
            if len(post.comments) == 0:  # Only add if no comments exist
                comment = Comment(
                    content=sample_comments[i % len(sample_comments)],
                    blog_id=post.id,
                    user_id=demo_user.id
                )
                db.session.add(comment)
        
        db.session.commit()
        print("✓ Added sample comments")
        
        # Show summary
        total_posts = BlogPost.query.count()
        total_comments = Comment.query.count()
        mood_counts = {}
        for mood in ['happy', 'sad', 'anxious', 'angry', 'neutral', 'excited']:
            count = BlogPost.query.filter_by(mood=mood).count()
            mood_counts[mood] = count
        
        print(f"\n📊 Blog Statistics:")
        print(f"   Total Posts: {total_posts}")
        print(f"   Total Comments: {total_comments}")
        print(f"   Mood Distribution:")
        for mood, count in mood_counts.items():
            emoji = {'happy': '😊', 'sad': '😢', 'anxious': '😰', 'angry': '😠', 'neutral': '😐', 'excited': '🤩'}
            print(f"     {emoji[mood]} {mood.title()}: {count}")
        
        print(f"\n🌟 Enhanced Blog Features Now Available:")
        print(f"   • Mood-based categorization and filtering")
        print(f"   • Dark/light theme toggle")
        print(f"   • Like/unlike posts functionality")
        print(f"   • Enhanced search and filtering")
        print(f"   • Crisis detection and support resources")
        print(f"   • Voice input support")
        print(f"   • Beautiful modern UI with animations")
        print(f"\n🚀 Visit http://localhost:5000/blog to explore!")

if __name__ == "__main__":
    create_demo_data()
