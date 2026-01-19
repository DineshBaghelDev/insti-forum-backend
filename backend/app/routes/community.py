from flask import Blueprint, request
from app.extensions import db
from app.models.community import Community

community_bp = Blueprint("community", __name__)

@community_bp.route("/communities", methods=["POST"])
def create_community():
    data = request.get_json()
    name = data.get("name")
    description = data.get("description")

    if not name:
        return {"error": "Community name is required"}, 400
    
    community = Community(name=name, description=description, creator_id=1) #to be changed
    db.session.add(community)
    db.session.commit()

    return {
        "message": "Community created successfully",
        "community_id": community.id
    }, 201
