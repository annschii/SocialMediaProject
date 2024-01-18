# app.py

from flask import Flask, request, jsonify, send_from_directory, abort
from werkzeug.utils import secure_filename
import os
from social_media_db import (
    initialize_db,
    insert_post, get_post_by_id, get_all_posts, update_post, delete_post,
    insert_user, get_all_users, get_user_by_id, update_user, delete_user
)
from flask_cors import CORS
import requests

app = Flask(__name__)

CORS(app, origins=["http://localhost:8000", "*"]) #for development

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

SENTIMENT_URL = os.environ.get("SENTIMENT_URL")


#define function to send request to sentiment_analyzer
def send_sentiment_analysis_request(text):
    # Set the URL based on the SENTIMENT_URL environment variable
    sentiment_url = SENTIMENT_URL + "analyze_sentiment"  # Replace with your actual endpoint if different

    # Prepare the payload for the POST request
    payload = {'text': text}

    try:
        # Send the POST request to the sentiment analysis API
        response = requests.post(sentiment_url, json=payload)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse and return the sentiment result
            result = response.json()
            return result['sentiment']
        else:
            # Handle unsuccessful request
            print(f"Error: {response.status_code}, {response.text}")
            return None
    except Exception as e:
        # Handle exceptions, e.g., network errors
        print(f"Exception: {str(e)}")
        return None

# Example usage:
sentiment_result = send_sentiment_analysis_request(text_to_analyze)



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

initialize_db()

@app.route('/posts', methods=['GET'])
def list_posts():
    filter_params = {k: v for k, v in request.args.items() if v is not None}
    posts = get_all_posts(filter_params)
    return jsonify([dict(post) for post in posts]), 200

@app.route('/posts', methods=['POST'])
def create_new_post():
    post_data = request.get_json()
    post_id = insert_post(post_data)
    sentiment_result = send_sentiment_analysis_request(post_data['text'])
    if post_id:
        return jsonify({"id": post_id, **post_data}), 201
    else:
        abort(500)

@app.route('/posts/<int:post_id>', methods=['GET'])
def get_post_detail(post_id):
    post = get_post_by_id(post_id)
    if post:
        return jsonify(post), 200
    else:
        abort(404)

@app.route('/posts/<int:post_id>', methods=['PATCH'])
def update_post_partial(post_id):
    update_data = request.get_json()
    if update_post(post_id, update_data):
        updated_post = get_post_by_id(post_id)
        return jsonify(updated_post), 200
    else:
        abort(400)

@app.route('/posts/<int:post_id>', methods=['PUT'])
def update_post_full(post_id):
    update_data = request.get_json()
    if update_post(post_id, update_data):
        updated_post = get_post_by_id(post_id)
        return jsonify(updated_post), 200
    else:
        abort(400)

@app.route('/posts/<int:post_id>', methods=['DELETE'])
def delete_post_endpoint(post_id):
    if delete_post(post_id):
        return jsonify({}), 204
    else:
        abort(404)

@app.route('/images', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join('/app/images', filename)
        file.save(file_path)
        return jsonify({'image_url': filename}), 201
    else:
        return jsonify({'message': 'Invalid file type'}), 400

@app.route('/images/<filename>')
def uploaded_file(filename):
    return send_from_directory('/app/images', filename)

@app.route('/users', methods=['GET'])
def list_users():
    id = request.args.get('id')
    username = request.args.get('username')
    first_name = request.args.get('first_name')
    last_name = request.args.get('last_name')
    email = request.args.get('email')

    filter_params = {k: v for k, v in request.args.items() if v is not None}
    users = get_all_users(filter_params)
    return jsonify(users), 200

@app.route('/users', methods=['POST'])
def create_user():
    user_data = request.get_json()
    user_id = insert_user(user_data)
    if user_id:
        return jsonify({"id": user_id, **user_data}), 201
    else:
        abort(500)

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = get_user_by_id(user_id)
    if user:
        return jsonify(user), 200
    else:
        abort(404)

@app.route('/users/<int:user_id>', methods=['PATCH'])
def update_user_partial(user_id):
    user_data = request.get_json()
    existing_user = get_user_by_id(user_id)
    if not existing_user:
        abort(404)

    updated_user = {**existing_user, **user_data}
    if update_user(user_id, updated_user):
        return jsonify(updated_user), 200
    else:
        abort(400)

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user_full(user_id):
    user_data = request.get_json()
    if not get_user_by_id(user_id):
        abort(404)

    if update_user(user_id, user_data):
        return jsonify(user_data), 200
    else:
        abort(400)

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user_endpoint(user_id):
    if delete_user(user_id):
        return jsonify({}), 204
    else:
        abort(404)

if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host='0.0.0.0',port=5000, debug=True) #the port must be specified when using docker