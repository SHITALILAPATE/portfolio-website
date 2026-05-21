"""
Shital Ilpate — Futuristic Portfolio (Flask)
Entry point. Creates the app, DB, login manager and registers blueprints.
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

    # ensure folders exist
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    os.makedirs(os.path.join(app.root_path, "database"), exist_ok=True)

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "info"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")

    with app.app_context():
        db.create_all()
        _seed_defaults()

    return app


def _seed_defaults():
    """Seed an admin user and starter projects on first run."""
    from werkzeug.security import generate_password_hash
    from models.models import Project

    if not User.query.filter_by(username="admin").first():
        admin = User(
            username="admin",
            email="admin@shital.dev",
            password=generate_password_hash("admin123"),
            is_admin=True,
        )
        db.session.add(admin)

    if Project.query.count() == 0:
        starters = [
            ("Typing Challenge Website",
             "Speed-test your typing with real-time WPM and accuracy charts.",
             "JavaScript, HTML, CSS",
             "https://github.com/", "#", "project1.png"),
            ("Aesthetic Chat Application",
             "Real-time chat with pastel bubbles and dreamy themes.",
             "Python, Flask, SQLite",
             "https://github.com/", "#", "project1.png"),
            ("Portfolio Website",
             "This very site — futuristic glassmorphism and neon glow.",
             "Flask, HTML, CSS, JS",
             "https://github.com/SHITALILAPATE/my-portfolio", "#", "project1.png"),
            ("E-commerce Fashion Website",
             "Shop UI with cart and elegant checkout.",
             "Flask, SQLite, Jinja",
             "https://github.com/", "#", "project1.png"),
            ("Cloud Dashboard",
             "Visualize cloud usage and costs in a neon analytics interface.",
             "Python, Flask, Chart.js",
             "https://github.com/", "#", "project1.png"),
            ("JavaScript Mini Projects",
             "A collection of bite-sized JS apps — calculators, todos, color pickers.",
             "JavaScript, HTML, CSS",
             "https://github.com/", "#", "project1.png"),
        ]
        for title, desc, stack, gh, demo, img in starters:
            db.session.add(Project(
                title=title, description=desc, tech_stack=stack,
                github_url=gh, demo_url=demo, image=img,
            ))

    db.session.commit()


app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5000)
