from flask import Flask
from flask_cors import CORS
from app.extensions import db, jwt, bcrypt
from app.config import Config

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config)

    print("JWT_SECRET_KEY =", app.config.get("JWT_SECRET_KEY"))

    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)

    from app.routes.auth import auth_bp
    from app.routes.community import community_bp
    from app.routes.post import post_bp
    from app.routes.comment import comment_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(community_bp)
    app.register_blueprint(post_bp)
    app.register_blueprint(comment_bp)

    return app
