from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models.user import User
from app.models.community import Community
from app.models.membership import CommunityMembership

community_bp = Blueprint("community", __name__)

@community_bp.route("/communities", methods=["POST"])
@jwt_required()
def create_community():
    data = request.get_json()
    name = data.get("name")
    description = data.get("description")
    creator_id = get_jwt_identity()
    # creator_id = 1

    if not name:
        return jsonify({"error": "Community name is required"}), 400

    community = Community(name=name, description=description, creator_id=creator_id)
    db.session.add(community)
    db.session.commit()

    return jsonify({
        "msg": "Success! Community created successfully.",
        "community_id": community.id
    }), 201

@community_bp.route("/communities", methods=["GET"])
def view_communities():
    communities = Community.query.all()
    community_list = []
    for i in communities:
        community_list.append({
            "id": i.id,
            "name": i.name,
            "description": i.description,
            "creator_id": i.creator_id,
            "created_at": i.created_at.isoformat(),
        })
    if not community_list:
        return jsonify({"error": "Oops! No communities found."}), 404
    return jsonify(community_list), 200

@community_bp.route("/communities/<int:community_id>", methods=["GET"])
def view_community(community_id):
    community = Community.query.get(community_id)
    if not community:
        return jsonify({"error": "Oops! Community not found"}), 404
    return jsonify({
        "id": community.id,
        "name": community.name,
        "description": community.description,
        "creator_id": community.creator_id,
        "created_at": community.created_at.isoformat(),
    }), 200

@community_bp.route("/communities/<int:community_id>/join", methods=["POST"])
@jwt_required()
def join_community(community_id):
    community = Community.query.get(community_id)
    user_id = get_jwt_identity()

    if not community:
        return jsonify({"error": "Oops! Community not found"}), 404
    
    check_existing = CommunityMembership.query.filter_by(community_id=community_id, user_id=user_id).first()
    if check_existing:
        return jsonify({"error": "You are already a member of this community"}), 400
    
    membership = CommunityMembership(community_id=community_id, user_id=user_id)
    db.session.add(membership)
    db.session.commit()
    return jsonify({
        "msg": f"Joined {community.name} successfully!",
        "membership_id": membership.id,
    }), 201

@community_bp.route("/communities/<int:community_id>/leave", methods=["POST"])
@jwt_required()
def leave_community(community_id):
    community = Community.query.get(community_id)
    user_id = get_jwt_identity()

    if not community:
        return jsonify({"error": "Oops! Community not found"}), 404
    
    membership = CommunityMembership.query.filter_by(community_id=community_id, user_id=user_id).first()
    if not membership:
        return jsonify({"error": "You are not a member of this community"}), 400
    
    db.session.delete(membership)
    db.session.commit()
    return jsonify({"msg": f"Left {community.name} successfully!"}), 204