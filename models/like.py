from extensions import db

likes = db.Table('likes',
    db.Column('user_id', db.String(36), db.ForeignKey('user.id'), primary_key=True),
    db.Column('post_id', db.String(36), db.ForeignKey('post.id'), primary_key=True)
)