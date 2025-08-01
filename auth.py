"""Secure authentication system for Travel AiGent with GDPR compliance."""
import os
import secrets
import time
import logging
from typing import Optional
from datetime import datetime, timedelta

from flask import session, request, jsonify, redirect, url_for
from functools import wraps
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError


class SimpleAuth:
    """Simple session-based authentication."""
    
    def __init__(self, app=None):
        self.app = app
        self.ph = PasswordHasher()
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize the auth system with Flask app."""
        self.app = app
        
        # Default admin credentials from environment
        self.admin_username = os.environ.get("ADMIN_USERNAME", "admin")
        
        # For existing deployments, check if using old hash format
        admin_password = os.environ.get("ADMIN_PASSWORD", "changeme123!")
        if admin_password.startswith("$argon2"):
            # Already hashed
            self.admin_password_hash = admin_password
        else:
            # Hash the plain password
            self.admin_password_hash = self._hash_password(admin_password)
        
        # Session settings with security
        app.config.setdefault("PERMANENT_SESSION_LIFETIME", 3600)  # 1 hour
        app.config.setdefault("SESSION_COOKIE_SECURE", True)  # HTTPS only
        app.config.setdefault("SESSION_COOKIE_HTTPONLY", True)  # No JS access
        app.config.setdefault("SESSION_COOKIE_SAMESITE", "Lax")  # CSRF protection
    
    def _hash_password(self, password: str) -> str:
        """Hash password with Argon2."""
        return self.ph.hash(password)
    
    def authenticate(self, username: str, password: str) -> bool:
        """Authenticate user credentials."""
        # First check if it's the admin user
        if username == self.admin_username:
            try:
                # Verify password with Argon2
                self.ph.verify(self.admin_password_hash, password)
                return True
            except VerifyMismatchError:
                return False
        
        # Check database for regular users
        from travel_aigent.models import User
        user = User.query.filter_by(username=username).first()
        
        if not user:
            return False
        
        try:
            # Verify password with Argon2
            self.ph.verify(user.password_hash, password)
            
            # Check if rehashing is needed
            if self.ph.check_needs_rehash(user.password_hash):
                user.password_hash = self.ph.hash(password)
                from travel_aigent.models import db
                db.session.commit()
            
            return True
        except VerifyMismatchError:
            return False
    
    def login(self, username: str, user_id: Optional[int] = None) -> None:
        """Log in user and create session."""
        session.permanent = True
        session['authenticated'] = True
        session['username'] = username
        session['login_time'] = time.time()
        if user_id:
            session['user_id'] = user_id
    
    def logout(self) -> None:
        """Log out user and clear session."""
        session.clear()
    
    def is_authenticated(self) -> bool:
        """Check if current user is authenticated."""
        if not session.get('authenticated'):
            return False
        
        # Check session timeout
        login_time = session.get('login_time', 0)
        if time.time() - login_time > 3600:  # 1 hour timeout
            self.logout()
            return False
        
        return True
    
    def get_current_user(self):
        """Get current user object, creating placeholder if needed."""
        if not self.is_authenticated():
            return None
            
        username = session.get('username')
        if not username:
            return None
            
        # Try to get user from database
        try:
            from travel_aigent.models import User, db
            user = User.query.filter_by(username=username).first()
            
            # If no user found, try to create admin user if it's the admin
            if not user and username == 'admin':
                # Try to create admin user
                try:
                    from travel_aigent import _ensure_admin_user
                    _ensure_admin_user()
                    # Commit the transaction to ensure the user is saved
                    db.session.commit()
                    # Try again
                    user = User.query.filter_by(username=username).first()
                except Exception as e:
                    logging.error(f"Failed to create admin user: {e}")
                    # Create a temporary user object for admin
                    class TempUser:
                        def __init__(self):
                            self.id = 0
                            self.username = 'admin'
                            self.email = 'admin@travelaigent.uk'
                            self.first_name = 'Admin'
                            self.last_name = 'User'
                            self.phone = ''
                            self.home_airports = ''
                            self.preferred_airlines = ''
                            self.dietary_restrictions = ''
                            self.travel_style = 'economy'
                            self.adults_count = 2
                            self.children_ages = ''
                            self.senior_travelers = False
                            self.preferred_accommodation = ''
                            self.created_at = datetime.now()
                            self.updated_at = datetime.now()
                        
                        def to_dict(self):
                            return {
                                'id': self.id,
                                'username': self.username,
                                'email': self.email,
                                'first_name': self.first_name,
                                'last_name': self.last_name
                            }
                    
                    user = TempUser()
                    # Don't add to session, just return for display
                    
            if not user:
                logging.warning(f"User {username} not found in database")
                return None
                
            return user
        except Exception as e:
            logging.error(f"Error getting current user: {e}")
            return None
    
    def require_auth(self, f):
        """Decorator to require authentication for routes."""
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not self.is_authenticated():
                if request.is_json:
                    return jsonify({'error': 'Authentication required'}), 401
                return redirect(url_for('auth.login'))
            return f(*args, **kwargs)
        return decorated_function


# Global auth instance
auth = SimpleAuth()


def require_auth(f):
    """Decorator for routes that require authentication."""
    return auth.require_auth(f)


def init_auth(app):
    """Initialize authentication with Flask app."""
    auth.init_app(app)
    return auth