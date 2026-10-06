import os
import sys

# Force UTF-8 stdout encoding on Windows
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from flask import Flask, render_template, session, g
from config import Config
from models import db
from models.user import User
from models.detection import Detection

from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.detection import detection_bp
from routes.admin import admin_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Ensure upload directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(os.path.join(app.config['BASE_DIR'], 'database'), exist_ok=True)

    # Initialize extensions
    db.init_app(app)

    # Register Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(detection_bp)
    app.register_blueprint(admin_bp)

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/about')
    def about():
        return render_template('about.html')

    @app.context_processor
    def inject_user():
        user = None
        if 'user_id' in session:
            user = User.query.get(session['user_id'])
        return dict(current_user=user)

    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('500.html'), 500

    @app.errorhandler(413)
    def request_entity_too_large(error):
        return render_template('413.html'), 413

    # Database Initialization & Seeding
    with app.app_context():
        db.create_all()
        # Seed default admin if no users exist
        if User.query.count() == 0:
            print("[DeepGuard AI] Seeding initial admin and demo user accounts...")
            admin_user = User(
                name="System Administrator",
                email="admin@deepguard.ai",
                role="admin"
            )
            admin_user.set_password("Admin@123")
            
            demo_user = User(
                name="Security Analyst",
                email="user@deepguard.ai",
                role="user"
            )
            demo_user.set_password("User@123")

            db.session.add(admin_user)
            db.session.add(demo_user)
            db.session.commit()
            print("[DeepGuard AI] Accounts initialized: admin@deepguard.ai / Admin@123, user@deepguard.ai / User@123")

    return app

app = create_app()

if __name__ == '__main__':
    print("=" * 60)
    print("[DEEPGUARD AI] Deepfake Detection System Server")
    print("Running on: http://127.0.0.1:5000")
    print("Admin login: admin@deepguard.ai | Password: Admin@123")
    print("User login:  user@deepguard.ai  | Password: User@123")
    print("=" * 60)
    app.run(host='127.0.0.1', port=5000, debug=True)
