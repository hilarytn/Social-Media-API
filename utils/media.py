# media.py
import cloudinary
import cloudinary.uploader
import cloudinary.api

# Upload media file to Cloudinary
def upload_media(file, folder="media"):
    if file:
        upload_result = cloudinary.uploader.upload(file, folder=folder)
        return upload_result.get('url')
    return None
