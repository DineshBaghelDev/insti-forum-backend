from app.extensions import db

class CommunityMembership(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id= db.Column(db.Integer)
    community_id = db.Column(db.Integer) 
