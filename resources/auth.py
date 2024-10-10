from flask import Blueprint, request, jsonify
from models.user import User
from extensions import db
from schemas.user_schema import UserSchema
from services.auth_service import create_access_token
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__)

user_schema = UserSchema()

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # Validate the input
    errors = user_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    # Check if email or username already exists
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"message": "Email already exists"}), 400
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"message": "Username already exists"}), 400

    # Create new user
    user = User(
        fullname=data['fullname'],
        username=data['username'],
        email=data['email']
    )

    # Hash the password
    user.set_password(data['password'])  

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully. Please log in."}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    user = User.query.filter(
        (User.email == data['email_or_username']) | 
        (User.username == data['email_or_username'])
        ).first()

    if not user or not user.check_password(data['password']):
        return jsonify({"message": "Invalid credentials"}), 401

    # if not user.is_verified:
    #     return jsonify({"message": "Please verify your email before logging in."}), 403

    access_token = create_access_token(identity=user.id)
    return jsonify({"access_token": access_token,
                    "id": user.id,
                    "fullname": user.fullname,
                    "username": user.username,
                    "email": user.email}), 200

@auth_bp.route('/all', methods=['GET'])
def all_users():
    users = User.query.all()
    users_list = [user.to_dict() for user in users]
    return jsonify(users_list)