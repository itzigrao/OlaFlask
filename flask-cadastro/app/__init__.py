import os

from dotenv import load_dotenv
from flask import Flask

from app.extensions import db, migrate

def create_app(test_config=None):

    load_dotenv()

    app = Flask(__name__)

    app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"

    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    migrate.init_app(app, db)

    from app.models import Usuario
    from app.routes.auth import auth_bp

    app.register_blueprint(auth_bp)


    return app