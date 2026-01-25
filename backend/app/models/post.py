from app.extensions import db

class Post(db.Model): 
  __tablename__ = "post"
  id = db.Column(db.Integer, primary_key = True) 
  user_id= db.Column(db.Integer, db.ForeignKey('user.id')) 
  community_id = db.Column(db.Integer, db.ForeignKey('community.id')) 
  title = db.Column(db.String(100), nullable=False) 
  content = db.Column(db.String(1000)) 
  created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
