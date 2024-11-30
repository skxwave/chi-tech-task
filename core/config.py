import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    TESTING = False
    SECRET_KEY = os.environ.get("SECRET_KEY", "test_secret_key")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "test_jwt_key")
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI", "sqlite:///")
