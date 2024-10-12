from flask import Blueprint, request, jsonify, current_app, url_for
from models.user import User
from extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity
import uuid

# Create the blueprint for profile-related routes
profile_bp = Blueprint('profile', __name__)

# View user profile
@profile_bp.route('/<string:user_id>', methods=['GET'])
@jwt_required()
def view_profile(user_id):
    # Ensure user_id is valid UUID
    try:
        uuid.UUID(user_id)
    except ValueError:
        return jsonify({"message": "Invalid user ID format"}), 400
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

@profile_bp.route('/edit', methods=['PUT'])
@jwt_required()
def edit_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({"message": "User not found"}), 404

    data = request.get_json()
    user.fullname = data.get('fullname', user.fullname)
    user.username = data.get('username', user.username)
    user.bio = data.get('bio', user.bio)
    user.profile_picture = data.get('profile_picture', user.profile_picture)
    user.personal_details = data.get('personal_details', user.personal_details)

    db.session.commit()
    
    return jsonify({"message": "Profile updated successfully"}), 200