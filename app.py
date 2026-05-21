"""
Shital Ilpate — Futuristic Portfolio (Flask)
"""

import os
from flask import Flask
from flask_login import LoginManager
from models.models import db, User
from instance.config import Config
from routes.main_routes import main_bp
from auth.routes import auth_bp


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    # create folders
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    os.makedirs(os.path.join(app.root_path, "database"), exist_ok=True)

    db.init_app(app)

    # login manager
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "info"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")

    with app.app_context():
        db.create_all()
        create_admin()

    return app


def create_admin():
    """Create admin only."""

    from werkzeug.security import generate_password_hash

    if not User.query.filter_by(username="admin").first():

        admin = User(
            username="admin",
            email="admin@shital.dev",
            password=generate_password_hash("admin123"),
            is_admin=True,
        )

        db.session.add(admin)
        db.session.commit()


app = create_app()

if __name__ == "__main__":
    app.run()