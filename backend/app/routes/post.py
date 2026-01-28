from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.user import User
from app.models.community import Community
from app.models.membership import CommunityMembership
from app.models.post import Post

post_bp = Blueprint("post", __name__)

@post_bp.route("/posts", methods=["POST"])
def create_post():
    data = request.get_json()
    user_id = 1 #to be changed
    community_id = data.get("community_id")
    is_member = CommunityMembership.query.filter_by(
        user_id=user_id, 
        community_id=community_id
    ).first()
    if is_member:
        name = data.get("name")
        description = data.get("description")
        title = data.get("title")
        content = data.get("content")
        if not community_id:
            return {"error": "Community ID is required"}, 400
     
        new_post = Post(
            user_id=user_id,
            community_id=community_id,
            title=title,
            content=content
            ) 
        db.session.add(new_post)
        db.session.commit()
        return {
            "message": "Success! Post created successfully.",
            "post_id": new_post.id
        }, 201
    else:
        return {"error": "You must be a member of the community to create a post."}, 403

@post_bp.route("/posts/<int:post_id>", methods=["GET"])
def view_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        return {"error": "Oops! Post not found"}, 404
    return jsonify({
        "id": post.id,
        "user_id": post.user_id,
        "community_id": post.community_id,
        "title": post.title,
        "content": post.content,
        "created_at": post.created_at.isoformat(),
    }), 200

@post_bp.route("/communities/<int:community_id>/posts", methods=["GET"])
def view_community_posts(community_id):
    posts = Post.query.filter_by(community_id=community_id).all()
    post_list = []
    for i in posts:
        post_list.append({
            "id": i.id,
            "user_id": i.user_id,
            "community_id": i.community_id,
            "title": i.title,
            "content": i.content,
            "created_at": i.created_at.isoformat(),
        })
    if not post_list:
        return {"error": "Oops! No posts found in this community."}, 404
    return post_list, 200

@post_bp.route("/posts/<int:post_id>", methods=["DELETE"])
def delete_post(post_id):
    user_id = get_jwt_identity()  
    post = Post.query.get(post_id)
    if not post:
        return {"error": "Oops! Post not found"}, 404
    if post.user_id != user_id:
        return {"error": "You are not authorized to delete this post."}, 403
    db.session.delete(post)
    db.session.commit()
    return {"message": "Success! Post deleted successfully."}, 200



