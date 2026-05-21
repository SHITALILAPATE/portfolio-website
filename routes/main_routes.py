"""Main blueprint — public pages, dashboard, project CRUD."""
import os
import uuid
from functools import wraps
from flask import (Blueprint, render_template, request, redirect, url_for,
                   flash, current_app, abort)
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from models.models import db, Project

main_bp = Blueprint("main", __name__)


def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return wrapper


def _allowed(filename):
    return ("." in filename and
            filename.rsplit(".", 1)[1].lower()
            in current_app.config["ALLOWED_EXTENSIONS"])


def _save_image(file_storage):
    """Save uploaded file safely; return stored filename or None."""
    if not file_storage or file_storage.filename == "":
        return None
    if not _allowed(file_storage.filename):
        flash("Unsupported image type", "error")
        return None
    ext = file_storage.filename.rsplit(".", 1)[1].lower()
    name = f"{uuid.uuid4().hex}.{ext}"
    file_storage.save(os.path.join(current_app.config["UPLOAD_FOLDER"], name))
    return f"uploads/{name}"


# ---------- Public pages ----------

@main_bp.route("/")
def index():
    projects = Project.query.order_by(Project.created_at.desc()).all()
    return render_template("index.html", projects=projects)


@main_bp.route("/about")
def about():
    return render_template("about.html")


@main_bp.route("/skills")
def skills():
    return render_template("skills.html")


@main_bp.route("/projects")
def projects():
    items = Project.query.order_by(Project.created_at.desc()).all()
    return render_template("projects.html", projects=items)


@main_bp.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()
        if not name or not email or not message:
            flash("Please fill out every field", "error")
        else:
            # TODO: hook up email sending or DB storage
            flash("Message sent! I'll get back to you soon ✨", "success")
            return redirect(url_for("main.contact"))
    return render_template("contact.html")


# ---------- Admin dashboard ----------

@main_bp.route("/dashboard")
@login_required
def dashboard():
    items = Project.query.order_by(Project.created_at.desc()).all()
    return render_template("dashboard.html", projects=items)


@main_bp.route("/dashboard/project/new", methods=["GET", "POST"])
@login_required
@admin_required
def new_project():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        tech = request.form.get("tech_stack", "").strip()
        github = request.form.get("github_url", "#").strip() or "#"
        demo = request.form.get("demo_url", "#").strip() or "#"
        if not title or not description or not tech:
            flash("Title, description and tech stack are required", "error")
            return redirect(url_for("main.new_project"))
        image = _save_image(request.files.get("image")) or "project1.png"
        db.session.add(Project(
            title=title, description=description, tech_stack=tech,
            github_url=github, demo_url=demo, image=image,
        ))
        db.session.commit()
        flash("Project added", "success")
        return redirect(url_for("main.dashboard"))
    return render_template("edit_project.html", project=None)


@main_bp.route("/dashboard/project/<int:pid>/edit", methods=["GET", "POST"])
@login_required
@admin_required
def edit_project(pid):
    project = Project.query.get_or_404(pid)
    if request.method == "POST":
        project.title = request.form.get("title", "").strip()
        project.description = request.form.get("description", "").strip()
        project.tech_stack = request.form.get("tech_stack", "").strip()
        project.github_url = request.form.get("github_url", "#").strip() or "#"
        project.demo_url = request.form.get("demo_url", "#").strip() or "#"
        new_image = _save_image(request.files.get("image"))
        if new_image:
            project.image = new_image
        db.session.commit()
        flash("Project updated", "success")
        return redirect(url_for("main.dashboard"))
    return render_template("edit_project.html", project=project)


@main_bp.route("/dashboard/project/<int:pid>/delete", methods=["POST"])
@login_required
@admin_required
def delete_project(pid):
    project = Project.query.get_or_404(pid)
    db.session.delete(project)
    db.session.commit()
    flash("Project deleted", "info")
    return redirect(url_for("main.dashboard"))
