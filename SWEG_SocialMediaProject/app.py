from flask import Flask, jsonify, request
from social_media_db import initialize_db, insert_post, get_latest_post, search_db_posts, get_post_by_id

app = Flask(__name__)

# Initialize the database
initialize_db()

@app.route('/posts', methods=['POST'])
def create_post():
    post_data = request.get_json()
    post_id = insert_post(post_data)
    if post_id:
        return jsonify({"id": post_id, **post_data}), 201
    else:
        return jsonify({"message": "Post could not be created"}), 500

@app.route('/posts/latest', methods=['GET'])
def latest_post():
    post = get_latest_post()
    if post:
        post_data = {
            'id': post[0],
            'image': post[1],
            'text': post[2],
            'user': post[3]
        }
        return jsonify(post_data), 200
    else:
        return jsonify({'message': 'No latest post found'}), 404

@app.route('/posts/search', methods=['GET'])
def search_posts():
    user = request.args.get('user')
    text = request.args.get('text')
    posts = search_db_posts(user=user, text=text)
    return jsonify(posts), 200

@app.route('/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = get_post_by_id(post_id)
    if post:
        post_data = {
            'id': post[0],
            'image': post[1],
            'text': post[2],
            'user': post[3]
        }
        return jsonify(post_data), 200
    else:
        return jsonify({'message': 'Post not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)


