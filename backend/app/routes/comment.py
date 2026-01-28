from flask import Blueprint, request
from app.extensions import db
from app.models.user import User
from app.models.comment import Comment
from app.models.post import Post

comment_bp = Blueprint("comment", __name__)

@comment_bp.route("/posts/<int:post_id>/comments", methods=["POST"])
def add_comment(post_id):
    data = request.get_json()
    content = data.get("content")
    user_id = 1 # to be changed

    if not content:
        return {"error" : "Comment must not be empty"}, 400

    post = Post.query.get(post_id)
    if not post:
        return {"error": "Oops! Post not found."}, 404

    comment = Comment(post_id=post_id, content=content, author_id=user_id)
    db.session.add(comment)
    db.session.commit()

    return{
        "message": "Success! Comment added successfully.",
        "comment_id": comment.id
    }, 201

@comment_bp.route("/posts/<int:post_id>/comments", methods=["GET"])
def view_comments(post_id):
    comments = Comment.query.filter_by(post_id=post_id).all()
    
    post = Post.query.get(post_id)
    if not post:
        return {"error": "Oops! Post not found."}, 404

    comments_list = []
    for i in comments:
        comments_list.append({
            "id": i.id,
            "post_id": i.post_id,
            "content": i.content,
            "author_id": i.author_id,
            "created_at": i.created_at.isoformat(),
        })
    return comments_list, 200
@comment_bp.route("posts/<int:post_id>/comments", methods = ["GET"])
def delete_comments(comment_id)
  user_id = get_jwt_identity()
  post_id = PO
