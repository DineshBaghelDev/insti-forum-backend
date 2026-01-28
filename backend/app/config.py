import os
from datetime import timedelta

class Config:

    SQLALCHEMY_DATABASE_URI = 'sqlite:///insti_forum.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=48)
