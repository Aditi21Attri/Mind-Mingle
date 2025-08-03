import sqlite3

connection = sqlite3.connect('instance/moodmingle.db')
cursor = connection.cursor()

# Check current columns
cursor.execute('PRAGMA table_info(blog_post)')
columns = [col[1] for col in cursor.fetchall()]
print(f'Current columns: {columns}')

try:
    if 'mood' not in columns:
        cursor.execute('ALTER TABLE blog_post ADD COLUMN mood VARCHAR(20)')
        print('Added mood column')
    
    if 'likes' not in columns:
        cursor.execute('ALTER TABLE blog_post ADD COLUMN likes INTEGER DEFAULT 0')  
        print('Added likes column')
        
    # Update existing posts
    cursor.execute('UPDATE blog_post SET mood = ? WHERE mood IS NULL', ('neutral',))
    cursor.execute('UPDATE blog_post SET likes = 0 WHERE likes IS NULL')
    
    connection.commit()
    print('Migration completed!')
    
    # Check final structure
    cursor.execute('PRAGMA table_info(blog_post)')
    final_columns = cursor.fetchall()
    print('Final table structure:')
    for col in final_columns:
        print(f'  {col[1]} - {col[2]}')
        
except Exception as e:
    print(f'Error: {e}')
    connection.rollback()
finally:
    connection.close()
