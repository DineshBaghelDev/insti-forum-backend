from app.extensions import db

class CommunityMembership(db.Model):
    __tablename__ = 'membership'
    id = db.Column(db.Integer, primary_key = True)
    user_id= db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    community_id = db.Column(db.Integer, db.ForeignKey('community.id'), nullable=False) 
