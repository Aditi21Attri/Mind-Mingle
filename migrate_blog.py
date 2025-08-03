#!/usr/bin/env python3
"""
Migration script to add mood and likes fields to BlogPost table
Run this script to update the database with new blog features
"""

import sqlite3
import os

def migrate_database():
    db_path = os.path.join('instance', 'moodmingle.db')
    
    if not os.path.exists(db_path):
        print("Database not found. Please run create_db.py first.")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("Starting blog table migration...")
        
        # Check if columns already exist
        cursor.execute("PRAGMA table_info(blog_post)")
        columns = [column[1] for column in cursor.fetchall()]
        print(f"Current columns: {columns}")
        
        # Add mood column if it doesn't exist
        if 'mood' not in columns:
            cursor.execute('ALTER TABLE blog_post ADD COLUMN mood VARCHAR(20)')
            print("✓ Added mood column to blog_post table")
        else:
            print("✓ Mood column already exists")
        
        # Add likes column if it doesn't exist
        if 'likes' not in columns:
            cursor.execute('ALTER TABLE blog_post ADD COLUMN likes INTEGER DEFAULT 0')
            print("✓ Added likes column to blog_post table")
        else:
            print("✓ Likes column already exists")
        
        # Create blog_likes association table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS blog_likes (
                user_id INTEGER NOT NULL,
                blog_post_id INTEGER NOT NULL,
                PRIMARY KEY (user_id, blog_post_id),
                FOREIGN KEY (user_id) REFERENCES user (id),
                FOREIGN KEY (blog_post_id) REFERENCES blog_post (id)
            )
        """)
        print("✓ Created blog_likes association table")
        
        # Update existing posts to have default mood 'neutral' if null
        cursor.execute('UPDATE blog_post SET mood = "neutral" WHERE mood IS NULL')
        affected_rows = cursor.rowcount
        print(f"✓ Updated {affected_rows} existing posts with default mood")
        
        # Update existing posts to have default likes 0 if null
        cursor.execute('UPDATE blog_post SET likes = 0 WHERE likes IS NULL')
        affected_rows = cursor.rowcount
        print(f"✓ Updated {affected_rows} existing posts with default likes")
        
        conn.commit()
        print("\n🎉 Blog migration completed successfully!")
        print("\nNew features available:")
        print("  • Mood categorization for posts")
        print("  • Like/unlike functionality")
        print("  • Enhanced filtering and search")
        print("  • Crisis detection and support")
        
        # Verify the migration
        cursor.execute("PRAGMA table_info(blog_post)")
        new_columns = cursor.fetchall()
        print(f"\nFinal table structure:")
        for col in new_columns:
            print(f"  {col[1]} - {col[2]}")
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        import traceback
        traceback.print_exc()
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_database()
