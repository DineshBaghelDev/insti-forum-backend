import email
from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models.user import User
from app.extensions import db, bcrypt
from app.utils.validators import check_user_input

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/auth/login', methods=['POST'])
def login():
    #if signing in from google"
    #elif signing in from apple":
    data = request.get_json()
    identifier = data.get('identifier')
    password = data.get('password')

    if not identifier:
        return jsonify({"msg": "Username or email is required"}), 400
    if not password:
        return jsonify({"msg": "Password is required"}), 400
    
    found_user = None
    found_user_by_email = User.query.filter_by(email = identifier).first()
    found_user_by_username = User.query.filter_by(username = identifier).first()
    if found_user_by_email:
        found_user = found_user_by_email
    elif found_user_by_username:
        found_user = found_user_by_username

    if found_user and bcrypt.check_password_hash(found_user.password_hash, password):
        access_token = create_access_token(identity=str(found_user.id))
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"msg": "Bad username or password"}), 401
    
@auth_bp.route('/auth/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    if not username:
        return jsonify({"msg": "Username is required"}), 400
    if not email:
        return jsonify({"msg": "Email is required"}), 400   
    if not password:
        return jsonify({"msg": "Password is required"}), 400

    is_valid, error_msg = check_user_input(email)

    if not is_valid:
        return jsonify({"msg": f"Invalid email address: {error_msg}"}), 400

    found_user_email = User.query.filter_by(email=email).first() 
    found_user_name = User.query.filter_by(username=username).first()
    if found_user_email or found_user_name:
        return jsonify({"msg": "User already exists"}), 409
    else:
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, email=email, password_hash=hashed_password)
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
        "name": user.username,
        "email": user.email,
        "created_at": user.created_at.isoformat(),
    }), 200



