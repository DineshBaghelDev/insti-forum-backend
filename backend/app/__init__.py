from flask import Flask
from app.extensions import db
from app.config import Config
# from app.models import Community, User

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    
    from app.routes.community import community_bp
    from app.routes.post import post_bp
    from app.routes.comment import comment_bp

    app.register_blueprint(community_bp)
    app.register_blueprint(post_bp)
    app.register_blueprint(comment_bp)


    # with app.app_context():
    #     from app.models.user import User
    #     from app.models.community import Community
    #     from app.models.membership import CommunityMembership
    # with app.app_context():
    #     from app import models
    return app