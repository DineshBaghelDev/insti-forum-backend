from app.extensions import db

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    post_id = db.Column(db.Integer)
    content = db.Column(db.String(200))
    author_id= db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
