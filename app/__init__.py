
from flask import Flask

from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from flask_login import LoginManager

from config import Config

db = SQLAlchemy()
moment = Moment()
bootstrap = Bootstrap()
login = LoginManager()
login.login_view = 'auth.login'


def create_app(config_class=Config):

    app = Flask(__name__)
    app.config.from_object(config_class)
    app.static_folder = config_class.STATIC_FOLDER
    app.template_folder = config_class.TEMPLATE_FOLDER
    
    db.init_app(app)
    moment.init_app(app)
    bootstrap.init_app(app)
    login.init_app(app)
    
    # blueprint registration
    from app.Controller.errors import bp_errors as errors
    from app.Controller.routes import bp_routes as routes
    from app.Controller.auth_routes import bp_auth as auth

    app.register_blueprint(errors)
    app.register_blueprint(routes)
    app.register_blueprint(auth)

    return app


