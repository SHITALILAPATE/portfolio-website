"""
Shital Ilpate — Futuristic Portfolio (Flask)
"""

import os
from flask import Flask
from flask_login import LoginManager
from models.models import db, User, Project
from instance.config import Config
from routes.main_routes import main_bp
from auth.routes import auth_bp


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(Config)

    # folders
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    os.makedirs(os.path.join(app.root_path, "database"), exist_ok=True)

    # database
    db.init_app(app)

    # login
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

    # create database
    with app.app_context():
        db.create_all()
        seed_projects()

    return app


def seed_projects():

    # ONLY add projects if database is empty
    if Project.query.count() == 0:

        projects = [

            Project(
                title="Kiki's Delivery Game",
                description="Fly on your broomstick",
                tech_stack="JavaScript, HTML, CSS",
                github_url="https://github.com/SHITALILAPATE",
                demo_url="#",
                image="kiki.png"
            ),

            Project(
                title="Calculator App",
                description="Simple aesthetic calculator app",
                tech_stack="HTML, CSS, JS",
                github_url="https://github.com/SHITALILAPATE",
                demo_url="#",
                image="calculator.png"
            ),

            Project(
                title="Portfolio Website",
                description="Futuristic developer portfolio",
                tech_stack="HTML, CSS, JS",
                github_url="https://github.com/SHITALILAPATE",
                demo_url="#",
                image="portfolio.png"
            ),

            Project(
                title="PhotoBooth",
                description="Photo booth using webcam filters",
                tech_stack="JavaScript, HTML, CSS, Python",
                github_url="https://github.com/SHITALILAPATE",
                demo_url="#",
                image="photobooth.png"
            ),

            Project(
                title="Pomodoro Timer",
                description="Focus timer productivity app",
                tech_stack="Python, Flask, HTML, CSS, JS",
                github_url="https://github.com/SHITALILAPATE",
                demo_url="#",
                image="pomodoro.png"
            ),

            Project(
                title="Habit Tracker",
                description="Track habits and progress",
                tech_stack="JavaScript, HTML, CSS, Python",
                github_url="https://github.com/SHITALILAPATE",
                demo_url="#",
                image="habit.png"
            ),

        ]

        db.session.add_all(projects)
        db.session.commit()


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)

