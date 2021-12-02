from flask.json import jsonify
from App.controllers.post import (create_new_post, delete_post_by_id, edit_post, get_post_by_id, get_user_posts)
from App.models import Post
from App.modules.serialization_module import serialize_list
from flask import Blueprint, request
from flask_jwt import jwt_required

post_views = Blueprint('post_views', __name__, template_folder='../templates')


# get post by id
@post_views.route('/posts/<int:post_id>', methods=["GET"])
def get_post(post_id):
    post = get_post_by_id(post_id)
    return jsonify(post.toDict())


# get all posts
@post_views.route("/posts", methods=["GET"])
@jwt_required
def get_all_posts():
    posts = Post.query.all()
    return jsonify(serialize_list(posts))


#get posts by user
@post_views.route("/posts/<int:user_id>", methods=["GET"])
@jwt_required()
def get_posts_by_user(user_id):
    try:
        posts = get_user_posts(user_id)
        return jsonify(serialize_list(posts))
    except Exception as e:
        print(e)
        return 500
    

@post_views.route("/posts", methods=["POST"])
@jwt_required()
def create_post():
    user_id = request.json.get("user_id")
    topic_id = request.json.get("topic_id")
    text = request.json.get("text")
    created_date = request.json.get("created_date")

    new_post = create_new_post(user_id, topic_id, text, created_date)
    return jsonify(new_post.toDict())


@post_views.route("/posts/<int:post_id>", methods=["PUT"])
@jwt_required()
def update_post(post_id):
    post_id = request.json.get("post_id")
    topic_id = request.json.get("topic_id")
    text = request.json.get("text")
    created_date = request.json.get("created_date")

    post = edit_post(post_id, topic_id, text, created_date)

    return jsonify(post.toDict()) if post else 404
    

@post_views.route("/posts/<int:post_id>", methods=["DELETE"])
@jwt_required()
def delete_post(post_id):
    result = delete_post_by_id(post_id)
    return jsonify(result.toDict()) if result else 404
