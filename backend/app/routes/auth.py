from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models.user import User
from app.extensions import db, bcrypt
from app.models.user import User

auth_bp = Blueprint(__name__)

users = {"testuser": bcrypt.generate_password_hash("testpass").decode('utf-8')}

@auth_bp.route('/auth/login', methods=['POST'])
def login():
    #if signing in from google"
    #elif signing in from apple":
    data = request.get_json()
    identifier = data.get('identifier')
    password = data.get('password')
    found_user_by_email = User.query.filter_by(email = identifier).first()
    found_user_by_name = User.query.filter_by(email = identifier).first()
    if found_user_by_email:
        found_user = found_user_by_email
    elif found_user_by_name:
        found_user = found_user_by_name

    if found_user and bcrypt.check_password_hash(found_user.password, password):
        access_token = create_access_token(identity=str(found_user.id))
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"msg": "Bad username or password"}), 401
    
@auth_bp.route('/auth/signup', methods=['POST'])
def signup():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    
    found_user_email = User.query.filter_by(email=email).first() 
    found_user_name = User.query.filter_by(name=name).first()
    if found_user_email or found_user_name:
        return jsonify({"msg": "User already exists"}), 409
    else:
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(name=name, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"msg": "User created successfully"}), 201
    
@auth_bp.route('/auth/me', methods=['GET'])
@jwt_required() 
def view_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404
    return jsonify({
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "created_at": user.created_at.isoformat(),
    }), 200
