from flask import Flask
from flask_cors import CORS

from core.config import Config
from core import db, jwt, swagger
from .auth import bp as authbp
from .articles import bp as articlesbp
from .users import bp as usersbp
from .commands import bp as adminbp

baseprefix = "/api/v1"


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    jwt.init_app(app)
    swagger.init_app(app)
    CORS(app)

    app.register_blueprint(authbp, url_prefix=f"{baseprefix}/auth")
    app.register_blueprint(articlesbp, url_prefix=f"{baseprefix}/articles")
    app.register_blueprint(usersbp, url_prefix=f"{baseprefix}/users")
    app.register_blueprint(adminbp)

    return app
