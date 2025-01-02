import json

from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.route('/api/posts', methods=['GET'])
def get_posts():
    return jsonify(POSTS)


@app.route("/api/posts", methods=["POST"])
def add_post():
    data = request.get_json()

    error_response = _validate_add_post(data)
    if error_response:  # If there's an error, return it
        return error_response

    new_id = get_new_id(POSTS)

    new_post = {
        "id": new_id,
        "title": data.get("title"),
        "content": data.get("content")
    }
    POSTS.append(new_post)

    return jsonify(new_post), 201

def _validate_add_post(data: dict):
    missing_fields = []
    if not data.get("title"):
        missing_fields.append("title")
    if not data.get("content"):
        missing_fields.append("content")

    if missing_fields:
        return jsonify({
            "error": "Bad Request",
            "message": f"Missing fields: {', '.join(missing_fields)}"
        }), 400
    return None  # No errors
def get_new_id(posts) -> int:
    return max([post["id"] for post in posts], default=0) + 1



@app.route("/api/posts/<int:id>", methods=["DELETE"])
def delete_post(id):

    post_to_delete = next((post for post in POSTS if post["id"] == id), None)

    if post_to_delete is None:
        return jsonify({
            "error": "Not Found",
            "message": f"Post with id {id} was not found."
        }), 404

    POSTS.remove(post_to_delete)

    return jsonify({
        "message": f"Post with id {id} has been deleted successfully."
    }), 200



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
