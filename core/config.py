import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()


class Config:
    TESTING = False
    SECRET_KEY = os.environ.get("SECRET_KEY", "test_secret_key")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "test_jwt_key")
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI", "sqlite:///")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=int(os.environ.get("JWT_ACCESS_TOKEN_EXPIRES_MINUTES", 30)))
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=int(os.environ.get("JWT_REFRESH_TOKEN_EXPIRES_DAYS", 3)))
    PAGE_SIZE = int(os.environ.get("PAGE_SIZE", 10))
