from app.extensions import db

class Community(db.Model):
    __tablename__ = 'community'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(200))
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
