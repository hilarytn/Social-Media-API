from flask import Blueprint, request, jsonify, current_app
from models.user import User
from extensions import db, mail
from schemas.user_schema import UserSchema
from services.auth_service import generate_access_token, generate_verification_token
from flask_jwt_extended import create_access_token
from utils.otp import generate_otp, send_otp_email

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

    # Generate verification token
    verification_token = generate_verification_token(user)
    user.verification_token = verification_token 

    db.session.add(user)
    db.session.commit()

    # Send verification email
    verification_link = url_for('auth.verify_email', token=verification_token, _external=True)
    msg = Message(subject="Email Verification", 
                  sender=current_app.config['MAIL_USERNAME'], 
                  recipients=[user.email])
    msg.body = f"Please click the link to verify your email: {verification_link}"
    
    try:
        mail.send(msg)
    except Exception as e:
        return jsonify({"message": f"Failed to send email: {str(e)}"}), 500

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

@auth_bp.route('/request_otp', methods=['POST'])
def request_otp():
    data = request.get_json()
    email = data.get('email')

    otp = generate_otp()

    # Send the OTP via email
    send_otp_email(email, otp)

    return {"msg": "OTP sent to your email."}, 200 