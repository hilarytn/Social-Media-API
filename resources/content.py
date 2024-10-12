# resources/content.py
from flask import Blueprint, request, jsonify
from models import Post
from extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.media import upload_media
from werkzeug.utils import secure_filename

content_bp = Blueprint('content', __name__)

# Create Post
@content_bp.route('/post', methods=['POST'])
@jwt_required()
def create_post():
    user_id = get_jwt_identity()
    data = request.form
    content = data.get('content')
    
    # Handle media file upload
    image_file = request.files.get('image_file')
    video_file = request.files.get('video_file')

    image_url = upload_media(image_file, folder="images") if image_file else None
    video_url = upload_media(video_file, folder="videos") if video_file else None

    if not content:
        return jsonify({"message": "Invalid post content."}), 400

    new_post = Post(
        content=content,
        image_url=image_url,
        video_url=video_url,
        user_id=user_id 
    )
    db.session.add(new_post)
    db.session.commit()

    return jsonify({"message": "Post created successfully.", "post_id": new_post.id}), 201
