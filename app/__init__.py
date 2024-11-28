from flask import Flask

from core.config import Config
from core import db, jwt
from .auth.views import bp as authbp
from .articles.views import bp as articlesbp
from .users.views import bp as usersbp

baseprefix = "/api/v1"


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(authbp, url_prefix=f"{baseprefix}/auth")
    app.register_blueprint(articlesbp, url_prefix=f"{baseprefix}/articles")
    app.register_blueprint(usersbp, url_prefix=f"{baseprefix}/users")

    return app
