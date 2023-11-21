import sqlite3

def initialize_db():
    conn = sqlite3.connect('social_media.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            image TEXT,
            text TEXT,
            user TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_post(post):
    conn = sqlite3.connect('social_media.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO posts (image, text, user) VALUES (?, ?, ?)
    ''', (post['image'], post['text'], post['user']))
    post_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return post_id

def get_latest_post():
    conn = sqlite3.connect('social_media.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM posts ORDER BY id DESC LIMIT 1
    ''')
    post = cursor.fetchone()
    conn.close()
    return post

def search_db_posts(user=None, text=None):
    conn = sqlite3.connect('social_media.db')
    cursor = conn.cursor()
    
    query = 'SELECT * FROM posts WHERE 1=1'
    params = []
    
    if user:
        query += ' AND user = ?'
        params.append(user)
    if text:
        query += ' AND text LIKE ?'
        params.append(f'%{text}%')
    
    cursor.execute(query, params)
    posts = cursor.fetchall()
    conn.close()
    
    return [{'id': post[0], 'image': post[1], 'text': post[2], 'user': post[3]} for post in posts]

def get_post_by_id(post_id):
    conn = sqlite3.connect('social_media.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM posts WHERE id = ?
    ''', (post_id,))
    post = cursor.fetchone()
    conn.close()
    return post
