"""Travel AiGent package initialization and Flask app factory."""
import logging
import os
import secrets
from pathlib import Path
from datetime import datetime

from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from logger import setup_logging
from .models import db
from auth import init_auth
from version import VERSION_FULL, get_version_info

# ----------------------------------------------------------------------------
# Helper Functions
# ----------------------------------------------------------------------------

def _ensure_admin_user():
    """Ensure admin user exists in database."""
    try:
        from .models import User
        from argon2 import PasswordHasher
        
        # Check if admin exists
        admin = User.query.filter_by(username='admin').first()
        
        if not admin:
            ph = PasswordHasher()
            
            # Get admin credentials from environment
            admin_username = os.environ.get("ADMIN_USERNAME", "admin")
            admin_password = os.environ.get("ADMIN_PASSWORD", "changeme123!")
            
            # Create admin user
            admin = User(
                username=admin_username,
                email='admin@travelaigent.com',
                password_hash=ph.hash(admin_password),
                first_name='Admin',
                last_name='User'
            )
            
            db.session.add(admin)
            db.session.commit()
            
            logging.info(f"Created admin user: {admin_username} (ID: {admin.id})")
        else:
            logging.info(f"Admin user exists: {admin.username} (ID: {admin.id})")
            
    except Exception as e:
        logging.error(f"Failed to ensure admin user: {e}")
        # Don't crash the app if admin user creation fails
        pass

# ----------------------------------------------------------------------------
# Application Factory
# ----------------------------------------------------------------------------

def create_app(config_overrides=None):
    """Create and configure a Flask application instance.

    Parameters
    ----------
    config_overrides
        Optional runtime configuration overrides that will be injected after
        default config has been loaded.

    Returns
    -------
    Flask
        Configured Flask app.
    """
    # Fix template path for deployment
    template_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates')
    static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static')
    app = Flask(__name__, 
                template_folder=template_dir,
                static_folder=static_dir,
                instance_relative_config=False)

    # ---------------------------------------------------------------------
    # Core configuration
    # ---------------------------------------------------------------------
    # Set application version
    app.config['VERSION'] = VERSION_FULL
    app.config['VERSION_INFO'] = get_version_info()
    
    # Secure secret key generation
    secret_key = os.environ.get("FLASK_SECRET_KEY")
    if not secret_key:
        # Generate a cryptographically secure secret key
        secret_key = secrets.token_hex(32)
        logging.warning("Using auto-generated secret key. Set FLASK_SECRET_KEY environment variable for production.")
    
    app.secret_key = secret_key
    
    # Database configuration - Railway provides DATABASE_URL automatically
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        # Fallback for local development
        database_url = "sqlite:///travel_aigent.db"
        logging.warning("No DATABASE_URL found, using SQLite for local development")
    
    # Fix postgres:// to postgresql:// for SQLAlchemy 1.4+
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
    }
    
    # Security configuration
    app.config["SESSION_COOKIE_SECURE"] = True if os.environ.get("FLASK_ENV") == "production" else False
    app.config["SESSION_COOKIE_HTTPONLY"] = True
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
    
    # Session configuration for persistent login
    app.config["SESSION_PERMANENT"] = True
    app.config["PERMANENT_SESSION_LIFETIME"] = 86400  # 24 hours

    if config_overrides:
        app.config.update(config_overrides)

    # ---------------------------------------------------------------------
    # Extensions & logging
    # ---------------------------------------------------------------------
    db.init_app(app)
    setup_logging()
    
    # CSRF protection disabled for now
    
    # Initialize authentication
    init_auth(app)
    
    # Initialize rate limiter
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        default_limits=["200 per day", "50 per hour"]
    )

    with app.app_context():
        db.create_all()
        logging.info(f"Database tables created successfully - TravelAiGent {VERSION_FULL}")
        
        # Ensure admin user exists
        _ensure_admin_user()
        
    # Make version available to all templates
    @app.context_processor
    def inject_version():
        return {'app_version': VERSION_FULL}
    
    # Security headers
    @app.after_request
    def security_headers(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        # Basic CSP - can be made more restrictive
        response.headers['Content-Security-Policy'] = "default-src 'self'; style-src 'self' 'unsafe-inline' fonts.googleapis.com cdnjs.cloudflare.com; font-src 'self' fonts.gstatic.com cdnjs.cloudflare.com; script-src 'self' 'unsafe-inline' cdn.jsdelivr.net; img-src 'self' data:;"
        return response

    # ---------------------------------------------------------------------
    # Simple health check route
    @app.route('/health')
    def health_check():
        from flask import jsonify
        return jsonify({
            'status': 'healthy', 
            'app': 'TravelAiGent',
            'version': VERSION_FULL
        }), 200
    
    # Debug route to check deployment
    @app.route('/version')
    def version_check():
        from flask import jsonify
        return jsonify({
            'version': VERSION_FULL,
            'build': get_version_info()['build'],
            'test_routes_available': True,
            'timestamp': datetime.utcnow().isoformat()
        }), 200

    # ---------------------------------------------------------------------
    # Register blueprints
    # ---------------------------------------------------------------------
    from .routes.status import bp as status_bp  # pylint: disable=import-outside-toplevel
    from .routes.briefs import bp as briefs_bp  # pylint: disable=import-outside-toplevel
    from .routes.deals import bp as deals_bp  # pylint: disable=import-outside-toplevel
    from .routes.auth import bp as auth_bp  # pylint: disable=import-outside-toplevel
    from .routes.profile import bp as profile_bp  # pylint: disable=import-outside-toplevel
    from .routes.groups import groups_bp  # pylint: disable=import-outside-toplevel
    from .routes.schools import schools  # pylint: disable=import-outside-toplevel
    from .routes.people import bp as people_bp  # pylint: disable=import-outside-toplevel
    from .routes.notifications import bp as notifications_bp  # pylint: disable=import-outside-toplevel
    from .routes.test_pages import bp as test_bp  # pylint: disable=import-outside-toplevel

    app.register_blueprint(auth_bp)
    app.register_blueprint(status_bp)
    app.register_blueprint(briefs_bp)
    app.register_blueprint(deals_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(groups_bp)
    app.register_blueprint(schools)
    app.register_blueprint(people_bp)
    app.register_blueprint(notifications_bp)
    app.register_blueprint(test_bp)

    return app


# Convenience for local `python -m travel_aigent` execution ------------------------------------------------

def run_dev() -> None:  # pragma: no cover
    """Run development server directly with `python -m travel_aigent`."""
    app = create_app()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)


if __name__ == "__main__":  # pragma: no cover
    run_dev()
