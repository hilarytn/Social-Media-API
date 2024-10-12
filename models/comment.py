from extensions import db
from datetime import datetime, timezone
import uuid

class Comment(db.Model):
    __tablename__ = 'comment'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    content = db.Column(db.Text, nullable=False)
    post_id = db.Column(db.String(36), db.ForeignKey('post.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    def __repr__(self):
        return f'<Comment {self.content[:20]}>'
