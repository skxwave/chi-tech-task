from flask import Flask

from core.config import Config
from core import db, jwt
from .auth.views import bp as authbp

baseprefix = "/api/v1"


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(authbp, url_prefix=f"{baseprefix}/auth")

    return app
