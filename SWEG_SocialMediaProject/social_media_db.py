# social_media_db.py

import sqlite3

DATABASE_NAME = 'social_media.db'


def get_db_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    # Create tables for posts and users
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            first_name TEXT,
            last_name TEXT,
            email TEXT NOT NULL
        )
    ''')
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            text TEXT,
            image TEXT,
            date_time DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    conn.commit()
    conn.close()


def insert_post(post):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO posts (user_id, text, image) VALUES (?, ?, ?)
    ''', (post['user_id'], post['text'], post['image']))
    post_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return post_id


def get_post_by_id(post_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM posts WHERE id = ?
    ''', (post_id,))
    post = cursor.fetchone()
    conn.close()
    return dict(post) if post else None


def get_all_posts(filter_params):
    conn = get_db_connection()
    cursor = conn.cursor()
    base_query = 'SELECT * FROM posts'
    where_clauses = []
    query_params = []
    for key, value in filter_params.items():
        if key == 'text':
            where_clauses.append(f"{key} LIKE ?")
            query_params.append(f"%{value}%")
        else:
            where_clauses.append(f"{key} = ?")
            query_params.append(value)
    if where_clauses:
        base_query += ' WHERE ' + ' AND '.join(where_clauses)
    cursor.execute(base_query, query_params)
    posts = cursor.fetchall()
    conn.close()
    return [dict(post) for post in posts]


def update_post(post_id, updated_post):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE posts
        SET user_id = ?, text = ?, image = ?
        WHERE id = ?
    ''', (updated_post['user_id'], updated_post['text'], updated_post['image'], post_id))
    changes = conn.total_changes
    conn.commit()
    conn.close()
    return changes > 0


def delete_post(post_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM posts WHERE id = ?', (post_id,))
    changes = conn.total_changes
    conn.commit()
    conn.close()
    return changes > 0


# ... (existing functions for working with posts)

def insert_user(user):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO users (username, first_name, last_name, email) VALUES (?, ?, ?, ?)
    ''', (user['username'], user['first_name'], user['last_name'], user['email']))
    user_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return user_id


def get_all_users(filter_params):
    conn = get_db_connection()
    cursor = conn.cursor()

    base_query = 'SELECT * FROM users'
    where_clauses = []
    query_params = []

    for key, value in filter_params.items():
        where_clauses.append(f"{key} = ?")
        query_params.append(value)

    if where_clauses:
        base_query += ' WHERE ' + ' AND '.join(where_clauses)

    cursor.execute(base_query, query_params)
    users = cursor.fetchall()
    conn.close()
    return [dict(user) for user in users]  # Convert sqlite3.Row to dict


def get_user_by_id(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    return dict(user) if user else None


def update_user(user_id, updated_user):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE users
        SET username = ?, first_name = ?, last_name = ?, email = ?
        WHERE id = ?
    ''', (
    updated_user['username'], updated_user['first_name'], updated_user['last_name'], updated_user['email'], user_id))
    changes = conn.total_changes
    conn.commit()
    conn.close()
    return changes > 0


def delete_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
    changes = conn.total_changes
    conn.commit()
    conn.close()
    return changes > 0


if __name__ == '__main__':
    initialize_db()  # Create tables if they don't exist.

    # Test insertion of dummy user.
    new_user = {
        'username': 'testuser',
        'first_name': 'Test',
        'last_name': 'User',
        'email': 'testuser@example.com'
    }
    print(f"Inserting user: {new_user}")
    user_id = insert_user(new_user)
    print(f"Inserted user with ID: {user_id}")

    # Fetch and print the inserted user.
    retrieved_user = get_user_by_id(user_id)
    print(f"Retrieved user: {retrieved_user}")