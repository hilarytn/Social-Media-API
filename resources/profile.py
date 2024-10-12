from flask import Blueprint, request, jsonify, current_app, url_for
from models.user import User
from extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity

# Create the blueprint for profile-related routes
profile_bp = Blueprint('profile', __name__)

# View user profile
@profile_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def view_profile(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    return jsonify({
        "id": user.id,
        "fullname": user.fullname,
        "username": user.username,
        "email": user.email,
        "bio": user.bio,
        "profile_picture": user.profile_picture,
        "personal_details": user.personal_details
    }), 200