from flask import Flask
from app.extensions import db
from app.config import Config
# from app.models import Community, User

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    
    from app.routes.community import community_bp
    app.register_blueprint(community_bp)
    # with app.app_context():
    #     from app import models
    return app