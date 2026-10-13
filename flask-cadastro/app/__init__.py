import os

from dotenv import load_dotenv
from flask import Flask

from app.extensions import db, migrate, login_manager

from .models import Usuario

def create_app(test_config=None):

    load_dotenv()

    app = Flask(__name__)

    app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"

    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    from app.models import Usuario
    from app.routes.auth import auth_bp
    from app.routes.__init__ import main_bp
    from app.routes.goal import goal_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(goal_bp)


    return app

@login_manager.user_loader
def load_user(usuario_id):
    return db.session.get(Usuario, int(usuario_id))