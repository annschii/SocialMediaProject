import sqlite3

def initialize_db():
    # Connect to SQLite database
    conn = sqlite3.connect('social_media.db')
    cursor = conn.cursor()

    # Create a table to store social media posts
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            image TEXT,
            text TEXT,
            user TEXT
        )
    ''')

    # Commit changes and close the connection
    conn.commit()
    conn.close()

def insert_posts(posts):
    # Connect to SQLite database
    conn = sqlite3.connect('social_media.db')
    cursor = conn.cursor()

    # Insert posts into the database
    for post in posts:
        cursor.execute('''
            INSERT INTO posts (image, text, user) VALUES (?, ?, ?)
        ''', (post['image'], post['text'], post['user']))

    # Commit changes and close the connection
    conn.commit()
    conn.close()

def get_latest_post():
    # Connect to SQLite database
    conn = sqlite3.connect('social_media.db')
    cursor = conn.cursor()

    # Retrieve the latest post
    cursor.execute('''
        SELECT * FROM posts ORDER BY id DESC LIMIT 1
    ''')
    latest_post = cursor.fetchone()

    # Close the connection
    conn.close()

    return latest_post
