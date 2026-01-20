from app.extensions import db

class Post(db.Model): 
  id = db.Column(db.Integer, primary_key = True) 
  user_id= db.Column(db.Integer) 
  community_id = db.Column(db.Integer) 
  title = db.Column(db.String(100)) 
  content = db.Column(db.String(1000)) 
  created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
