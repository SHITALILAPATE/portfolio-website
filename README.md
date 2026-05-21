# Shital Ilpate — Futuristic Portfolio (Flask)

A cute, futuristic, glassmorphism portfolio with:
- Animated typing hero, pastel neon glow, floating particles, cursor glow
- Login / signup (Flask-Login + hashed passwords)
- Admin dashboard to add / edit / delete projects with image uploads
- SQLite database (auto-created on first run)
- Deployment-ready (Procfile, runtime.txt, gunicorn)

## Quick start

```bash
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open http://localhost:5000

**Default admin** (created on first run):
- username: `admin`
- password: `admin123`
(change it from the dashboard after first login!)

## Project structure

```
portfolio-website/
├── app.py              # entry point
├── instance/config.py  # app config
├── models/models.py    # User + Project models
├── auth/               # login / signup
├── routes/             # public pages + dashboard CRUD
├── templates/          # Jinja2 templates
├── static/             # css / js / images
└── database/           # SQLite db (auto-created)
```

## Deployment

Works on any Python host (Render, Railway, Fly, Heroku):

```
gunicorn app:app
```

Remember to set `SECRET_KEY` in your host's environment variables.

## Notes

- Add your profile photo at `static/images/profile.jpg`
- Default project thumbnail: `static/images/project1.png`
- Upload form auto-saves images into `static/images/uploads/`
- Max upload size: 5 MB · allowed: png/jpg/jpeg/gif/webp
