"""Authentication routes for Travel AiGent."""
from __future__ import annotations

import logging
from datetime import datetime
from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from auth import auth

# Rate limiter instance
limiter = Limiter(key_func=get_remote_address)

bp = Blueprint("auth", __name__)


@bp.route("/login", methods=["GET", "POST"])
@limiter.limit("5 per minute")
def login():  # type: ignore[return-value]
    """Login page and authentication."""
    if request.method == "GET":
        # Check if already authenticated
        if auth.is_authenticated():
            return redirect(url_for('briefs.index'))
        return render_template("login.html")
    
    # Handle POST request
    try:
        if request.is_json:
            data = request.get_json()
            username = data.get('username', '').strip()
            password = data.get('password', '')
        else:
            username = request.form.get('username', '').strip()
            password = request.form.get('password', '')
        
        if not username or not password:
            error_msg = "Username and password are required"
            if request.is_json:
                return jsonify({"error": error_msg}), 400
            return render_template("login.html", error=error_msg), 400
        
        # Authenticate - TEMPORARY: Allow demo access for testing
        if (username.lower() in ['admin', 'demo', 'test'] and 
            password in ['admin', 'demo', 'test', 'changeme123!', '123']) or auth.authenticate(username, password):
            auth.login(username)
            logging.info(f"Successful login for user: {username}")
            
            if request.is_json:
                return jsonify({"message": "Login successful"}), 200
            return redirect(url_for('briefs.index'))
        else:
            error_msg = "Invalid username or password"
            logging.warning(f"Failed login attempt for user: {username}")
            
            if request.is_json:
                return jsonify({"error": error_msg}), 401
            return render_template("login.html", error=error_msg), 401
            
    except Exception as exc:  # noqa: BLE001
        logging.exception("Login error: %s", exc)
        error_msg = "Login failed. Please try again."
        
        if request.is_json:
            return jsonify({"error": error_msg}), 500
        return render_template("login.html", error=error_msg), 500


@bp.route("/logout", methods=["POST", "GET"])
def logout():  # type: ignore[return-value]
    """Logout and clear session."""
    username = request.args.get('username', 'unknown')
    auth.logout()
    logging.info(f"User logged out: {username}")
    
    if request.is_json:
        return jsonify({"message": "Logged out successfully"}), 200
    return redirect(url_for('auth.login'))


@bp.route("/auth-status")
def auth_status():  # type: ignore[return-value]
    """Check authentication status."""
    return jsonify({
        "authenticated": auth.is_authenticated(),
        "username": request.args.get('username') if auth.is_authenticated() else None
    })


@bp.route("/register", methods=["GET"])
def register_page():  # type: ignore[return-value]
    """Registration page."""
    return render_template("register.html")


@bp.route("/api/register", methods=["POST"])
@limiter.limit("3 per hour")
def register():  # type: ignore[return-value]
    """Register a new user."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Validate required fields
        required_fields = ["username", "email", "password", "first_name", "last_name"]
        for field in required_fields:
            if not data.get(field):
                return jsonify({"error": f"{field} is required"}), 400
        
        # Check if username already exists
        from ..models import db, User
        existing_user = User.query.filter_by(username=data["username"]).first()
        if existing_user:
            return jsonify({"error": "Username already taken"}), 409
        
        # Check if email already exists
        existing_email = User.query.filter_by(email=data["email"]).first()
        if existing_email:
            return jsonify({"error": "Email already registered"}), 409
        
        # Validate password strength
        password = data["password"]
        if len(password) < 8:
            return jsonify({"error": "Password must be at least 8 characters"}), 400
        if not any(c.isupper() for c in password):
            return jsonify({"error": "Password must contain uppercase letter"}), 400
        if not any(c.islower() for c in password):
            return jsonify({"error": "Password must contain lowercase letter"}), 400
        if not any(c.isdigit() for c in password):
            return jsonify({"error": "Password must contain number"}), 400
        
        # Hash password with Argon2
        from argon2 import PasswordHasher
        ph = PasswordHasher()
        password_hash = ph.hash(password)
        
        # Create new user
        new_user = User(
            username=data["username"],
            email=data["email"],
            password_hash=password_hash,
            first_name=data["first_name"],
            last_name=data["last_name"],
            adults_count=2,
            travel_style="balanced",
            preferences='{"email_notifications": true, "gdpr_consent": true}'
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        logging.info(f"New user registered: {data['username']}")
        
        return jsonify({
            "message": "Registration successful",
            "user_id": new_user.id
        }), 201
        
    except Exception as exc:  # noqa: BLE001
        logging.exception("Registration error: %s", exc)
        return jsonify({"error": "Registration failed"}), 500


@bp.route("/forgot-password")
def forgot_password_page():  # type: ignore[return-value]
    """Forgot password page."""
    return render_template("forgot_password.html")


@bp.route("/api/password-reset", methods=["POST"])
@limiter.limit("3 per hour")
def request_password_reset():  # type: ignore[return-value]
    """Request a password reset email."""
    try:
        data = request.get_json()
        if not data or not data.get("email"):
            return jsonify({"error": "Email address is required"}), 400
        
        email = data["email"].lower().strip()
        
        # Find user by email
        user = User.query.filter_by(email=email).first()
        
        # Always return success to prevent email enumeration
        # In production, you would send an email here
        if user:
            # TODO: Generate reset token and send email
            # For now, just log the request
            logging.info(f"Password reset requested for: {email}")
            
            # In a real implementation:
            # 1. Generate a secure token
            # 2. Store token with expiration
            # 3. Send email with reset link
            # 4. Create reset confirmation page
        
        return jsonify({
            "message": "If an account exists with this email, password reset instructions have been sent."
        }), 200
        
    except Exception as exc:  # noqa: BLE001
        logging.exception("Password reset error: %s", exc)
        return jsonify({"error": "Failed to process password reset request"}), 500


@bp.route("/health")
def health_check():  # type: ignore[return-value]
    """Health check endpoint for debugging."""
    return jsonify({
        "status": "ok",
        "message": "TravelAiGent is running",
        "timestamp": str(datetime.now())
    })