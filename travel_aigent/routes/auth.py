"""Authentication routes for Travel AiGent."""
from __future__ import annotations

import logging
from datetime import datetime
from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from argon2 import PasswordHasher

from auth import auth
from ..models import db, User, PasswordResetToken
from ..services.notifications import notification_service

bp = Blueprint("auth", __name__)


@bp.route("/login", methods=["GET", "POST"])
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
        
        # Authenticate user
        if auth.authenticate(username, password):
            # Get user from database to get user_id
            from ..models import User
            user = User.query.filter_by(username=username).first()
            user_id = user.id if user else None
            
            auth.login(username, user_id)
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
        
        # Send welcome email to new user
        try:
            subject = "Welcome to TravelAiGent!"
            html_content = f"""
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <h1 style="color: #C9A96E; text-align: center;">Welcome to TravelAiGent!</h1>
                
                <p style="color: #666; font-size: 16px;">
                    Hi {new_user.first_name},
                </p>
                
                <p style="color: #666; font-size: 16px;">
                    Thank you for joining TravelAiGent! Your account has been successfully created.
                </p>
                
                <div style="background: #f9f9f9; padding: 20px; border-radius: 10px; margin: 20px 0;">
                    <h3 style="color: #333; margin-top: 0;">Your Account Details:</h3>
                    <p style="color: #666; margin: 5px 0;"><strong>Username:</strong> {new_user.username}</p>
                    <p style="color: #666; margin: 5px 0;"><strong>Email:</strong> {new_user.email}</p>
                    <p style="color: #666; margin: 5px 0;"><strong>Name:</strong> {new_user.first_name} {new_user.last_name}</p>
                </div>
                
                <h3 style="color: #333;">Get Started:</h3>
                <ol style="color: #666; font-size: 16px;">
                    <li>Create a Travel Group to organize your trips</li>
                    <li>Add Travel Briefs to specify your destination preferences</li>
                    <li>We'll search for amazing deals and notify you when we find them!</li>
                </ol>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="{request.host_url}login" style="display: inline-block; background: #C9A96E; color: white; padding: 12px 30px; text-decoration: none; border-radius: 25px;">
                        Start Exploring Deals
                    </a>
                </div>
                
                <p style="color: #999; font-size: 14px; text-align: center;">
                    If you have any questions, feel free to reach out to our support team.
                </p>
            </div>
            """
            
            text_content = f"""
            Welcome to TravelAiGent!
            
            Hi {new_user.first_name},
            
            Thank you for joining TravelAiGent! Your account has been successfully created.
            
            Your Account Details:
            - Username: {new_user.username}
            - Email: {new_user.email}
            - Name: {new_user.first_name} {new_user.last_name}
            
            Get Started:
            1. Create a Travel Group to organize your trips
            2. Add Travel Briefs to specify your destination preferences
            3. We'll search for amazing deals and notify you when we find them!
            
            Login here: {request.host_url}login
            
            If you have any questions, feel free to reach out to our support team.
            """
            
            notification_service.send_email(
                to_email=new_user.email,
                subject=subject,
                html_content=html_content,
                text_content=text_content
            )
            logging.info(f"Welcome email sent to: {new_user.email}")
        except Exception as email_error:
            # Log error but don't fail registration
            logging.error(f"Failed to send welcome email: {email_error}")
        
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
        if user:
            # Create reset token
            reset_token = PasswordResetToken.create_token(user.id)
            
            # Generate reset URL
            reset_url = f"{request.host_url}reset-password?token={reset_token.token}"
            
            # Send email
            subject = "Reset Your TravelAiGent Password"
            html_content = f"""
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <h2 style="color: #C9A96E;">Password Reset Request</h2>
                
                <p style="color: #666; font-size: 16px;">
                    Hi {user.first_name or 'there'},
                </p>
                
                <p style="color: #666; font-size: 16px;">
                    We received a request to reset your TravelAiGent password. Click the button below to create a new password:
                </p>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="{reset_url}" style="display: inline-block; background: #C9A96E; color: white; padding: 12px 30px; text-decoration: none; border-radius: 25px;">
                        Reset Password
                    </a>
                </div>
                
                <p style="color: #666; font-size: 14px;">
                    Or copy and paste this link into your browser:<br>
                    <a href="{reset_url}" style="color: #C9A96E;">{reset_url}</a>
                </p>
                
                <p style="color: #999; font-size: 14px; margin-top: 30px;">
                    This link will expire in 1 hour for security reasons.
                </p>
                
                <p style="color: #999; font-size: 14px;">
                    If you didn't request this password reset, please ignore this email. Your password won't be changed.
                </p>
            </div>
            """
            
            text_content = f"""
            Hi {user.first_name or 'there'},
            
            We received a request to reset your TravelAiGent password.
            
            Reset your password here: {reset_url}
            
            This link will expire in 1 hour.
            
            If you didn't request this password reset, please ignore this email.
            """
            
            notification_service.send_email(
                to_email=user.email,
                subject=subject,
                html_content=html_content,
                text_content=text_content
            )
            
            logging.info(f"Password reset email sent to: {email}")
        
        return jsonify({
            "message": "If an account exists with this email, password reset instructions have been sent."
        }), 200
        
    except Exception as exc:  # noqa: BLE001
        logging.exception("Password reset error: %s", exc)
        return jsonify({"error": "Failed to process password reset request"}), 500


@bp.route("/reset-password")
def reset_password_page():  # type: ignore[return-value]
    """Password reset page."""
    token = request.args.get('token')
    if not token:
        return render_template("error.html", error="Invalid password reset link"), 400
    return render_template("reset_password.html", token=token)


@bp.route("/api/reset-password", methods=["POST"])
def reset_password():  # type: ignore[return-value]
    """Reset password with valid token."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
            
        token = data.get("token")
        new_password = data.get("password")
        
        if not token or not new_password:
            return jsonify({"error": "Token and new password are required"}), 400
        
        # Find and validate token
        reset_token = PasswordResetToken.query.filter_by(token=token).first()
        
        if not reset_token or not reset_token.is_valid():
            return jsonify({"error": "Invalid or expired reset token"}), 400
        
        # Validate password strength
        if len(new_password) < 8:
            return jsonify({"error": "Password must be at least 8 characters"}), 400
        if not any(c.isupper() for c in new_password):
            return jsonify({"error": "Password must contain uppercase letter"}), 400
        if not any(c.islower() for c in new_password):
            return jsonify({"error": "Password must contain lowercase letter"}), 400
        if not any(c.isdigit() for c in new_password):
            return jsonify({"error": "Password must contain number"}), 400
        
        # Update user password
        user = reset_token.user
        ph = PasswordHasher()
        user.password_hash = ph.hash(new_password)
        
        # Mark token as used
        reset_token.used = True
        
        db.session.commit()
        
        logging.info(f"Password reset successful for user: {user.username}")
        
        return jsonify({
            "message": "Password reset successful. You can now login with your new password."
        }), 200
        
    except Exception as exc:  # noqa: BLE001
        logging.exception("Password reset error: %s", exc)
        return jsonify({"error": "Failed to reset password"}), 500


@bp.route("/health")
def health_check():  # type: ignore[return-value]
    """Health check endpoint for debugging."""
    return jsonify({
        "status": "ok",
        "message": "TravelAiGent is running",
        "timestamp": str(datetime.now())
    })