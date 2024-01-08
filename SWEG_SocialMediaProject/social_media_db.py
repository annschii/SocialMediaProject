# social_media_db.py

#import sqlite3
import os
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv

load_dotenv()

DATABASE_NAME = os.environ.get("DATABASE_NAME")
DATABASE_URL = os.environ.get("DATABASE_URL")

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = True
    return conn


def initialize_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    # Create tables for posts and users
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username TEXT NOT NULL,
            first_name TEXT,
            last_name TEXT,
            email TEXT NOT NULL
        )
    ''')
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS posts (
            id SERIAL PRIMARY KEY,
            user_id INTEGER,
            text TEXT,
            image TEXT,
            date_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    conn.close()


def insert_post(post):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = sql.SQL('''
        INSERT INTO posts (user_id, text, image) VALUES (%s, %s, %s) RETURNING id
    ''')
    cursor.execute(query, (post['user_id'], post['text'], post['image']))
    post_id = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return post_id


def get_post_by_id(post_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM posts WHERE id = %s
    ''',(post_id,))
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
            where_clauses.append(f"{key} ILIKE %s")
            query_params.append(f"%{value}%")
        else:
            where_clauses.append(f"{key} =%s")
            query_params.append(value)
    if where_clauses:
        base_query += ' WHERE ' + ' AND '.join(where_clauses)
   
    cursor.execute(base_query + '', query_params)
    posts = cursor.fetchall()
    conn.close()
    #return [dict(post) for post in posts]
    post_dicts = [dict(zip([desc[0] for desc in cursor.description], post)) for post in posts]
    return post_dicts


def update_post(post_id, updated_post):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE posts
        SET user_id = %s, text = %s, image = %s
        WHERE id = %s
    ''', (updated_post['user_id'], updated_post['text'], updated_post['image'], post_id))
    changes = cursor.rowcount
    conn.commit()
    conn.close()
    return changes > 0


def delete_post(post_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM posts WHERE id = %s', (post_id,))
    changes = cursor.rowcount
    conn.commit()
    conn.close()
    return changes > 0


# ... (existing functions for working with posts)

def insert_user(user):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = sql.SQL('''
        INSERT INTO users (username, first_name, last_name, email) 
                    VALUES (%s, %s, %s, %s) RETURNING id
    ''')
    cursor.execute(query, (user['username'], user['first_name'], user['last_name'], user['email']))
    user_id = cursor.fetchone()[0]
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
        where_clauses.append(f"{key} = %s")
        query_params.append(value)

    if where_clauses:
        base_query += ' WHERE ' + ' AND '.join(where_clauses)

    cursor.execute(base_query, query_params)
    users = cursor.fetchall()
    conn.close()
    #return [dict(user) for user in users]  # Convert sqlite3.Row to dict
    return [dict(zip([desc[0] for desc in cursor.description], user)) for user in users]



def get_user_by_id(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
    user = cursor.fetchone()
    conn.close()
    return dict(user) if user else None


def update_user(user_id, updated_user):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = sql.SQL('''
        UPDATE users
        SET username = %s, first_name = %s, last_name = %s, email = %s
        WHERE id = %s
    ''')
    cursor.execute(query, (
    updated_user['username'], updated_user['first_name'], updated_user['last_name'], updated_user['email'], user_id))
    changes = cursor.rowcount
    conn.commit()
    conn.close()
    return changes > 0


def delete_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = sql.SQL('DELETE FROM posts WHERE user_id = %s')
    cursor.execute(query,(user_id,))
    query = sql.SQL('DELETE FROM users WHERE id = %s')
    cursor.execute(query, (user_id,))
    changes = cursor.rowcount
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