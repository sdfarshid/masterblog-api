import json
from typing import Union

from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


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
    post_to_delete = fetch_post_by_id(id)

    if post_to_delete is None:
        return jsonify({
            "error": "Not Found",
            "message": f"Post with id {id} was not found."
        }), 404

    POSTS.remove(post_to_delete)

    return jsonify({
        "message": f"Post with id {id} has been deleted successfully."
    }), 200


def fetch_post_by_id(post_id: int) -> Union[dict, None]:
    return next((post for post in POSTS if post["id"] == post_id), None)


@app.route("/api/posts/<int:id>", methods=["PUT"])
def update_post(id):
    post_to_update = fetch_post_by_id(id)

    if post_to_update is None:
        return jsonify({
            "error": "Not Found",
            "message": f"Post with id {id} was not found."
        }), 404

    data = request.get_json()

    post_to_update["title"] = data.get("title", post_to_update["title"])
    post_to_update["content"] = data.get("content", post_to_update["content"])

    # Return the updated post
    return jsonify(post_to_update), 200


@app.route("/api/posts/search", methods=["GET"])
def search_posts():
    title_query = request.args.get("title", "")
    content_query = request.args.get("content", "")

    matching_posts = [
        post for post in POSTS
        if (title_query and title_query.lower() in post["title"].lower())
           or (content_query and content_query.lower() in post["content"].lower())
    ]

    return jsonify(matching_posts), 200


@app.route('/api/posts', methods=['GET'])
def get_posts():
    sort_field = request.args.get('sort')
    direction = request.args.get('direction')

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 3, type=int)

    start = (page - 1) * per_page
    end = start + per_page

    if sort_field and sort_field not in ['title', 'content']:
        return jsonify({"error": "Bad Request", "message": "Invalid sort field. Use 'title' or 'content'."}), 400
    if direction and direction not in ['asc', 'desc']:
        return jsonify({"error": "Bad Request", "message": "Invalid direction. Use 'asc' or 'desc'."}), 400

    sorted_posts = POSTS[:]

    if sort_field:
        reverse = True if direction == 'desc' else False
        sorted_posts = sorted(POSTS, key=lambda post: post[sort_field].lower(), reverse=reverse)

    posts_page = sorted_posts[start:end]

    return jsonify(posts_page)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
