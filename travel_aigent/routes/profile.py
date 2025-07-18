"""User profile routes for Travel AiGent."""
from __future__ import annotations

import json
import logging
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from auth import require_auth, auth
from ..models import db, User

# Rate limiter instance
limiter = Limiter(key_func=get_remote_address)

bp = Blueprint("profile", __name__)


@bp.route("/profile")
@require_auth
def profile():  # type: ignore[return-value]
    """User profile page."""
    try:
        # Get current user (for now using username from session)
        username = request.args.get('username', 'admin')
        user = User.query.filter_by(username=username).first()
        
        if not user:
            # Create default user if doesn't exist
            user = User(
                username=username,
                email=f"{username}@travelaigent.com",
                password_hash="temp_hash",
                first_name="",
                last_name="",
                adults_count=2,
                travel_style="luxury"
            )
            db.session.add(user)
            db.session.commit()
        
        return render_template("profile.html", user=user)
    except Exception as exc:  # noqa: BLE001
        logging.exception("Error loading profile: %s", exc)
        return render_template("error.html", message="Unable to load profile"), 500


@bp.route("/groups")
@require_auth
def travel_groups():  # type: ignore[return-value]
    """Travel groups management page."""
    try:
        # Get current user (for now using username from session)
        username = request.args.get('username', 'admin')
        user = User.query.filter_by(username=username).first()
        
        if not user:
            # Create default user if doesn't exist
            user = User(
                username=username,
                email=f"{username}@travelaigent.com",
                password_hash="temp_hash",
                first_name="",
                last_name="",
                adults_count=2,
                travel_style="luxury"
            )
            db.session.add(user)
            db.session.commit()
        
        return render_template("groups.html", user=user)
    except Exception as exc:  # noqa: BLE001
        logging.exception("Error loading groups: %s", exc)
        return render_template("error.html", message="Unable to load groups"), 500


@bp.route("/api/profile", methods=["GET", "PUT"])
@require_auth
def api_profile():  # type: ignore[return-value]
    """API endpoint for profile data."""
    try:
        username = session.get('username', 'admin')
        user = User.query.filter_by(username=username).first()
        
        if request.method == "GET":
            if not user:
                # Create default user
                user = User(
                    username=username,
                    email=f"{username}@travelaigent.com",
                    password_hash="temp_hash",
                    first_name="",
                    last_name="",
                    adults_count=2,
                    travel_style="luxury"
                )
                db.session.add(user)
                db.session.commit()
            return jsonify(user.to_dict())
        
        # Handle PUT request
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        if not user:
            # Create new user
            user = User(
                username=username,
                email=f"{username}@travelaigent.com",
                password_hash="temp_hash"
            )
            db.session.add(user)
        
        # Update user fields
        if 'first_name' in data:
            user.first_name = data['first_name']
        if 'last_name' in data:
            user.last_name = data['last_name']
        if 'email' in data:
            user.email = data['email']
        if 'phone' in data:
            user.phone = data['phone']
        if 'home_airports' in data:
            user.home_airports = json.dumps(data['home_airports']) if isinstance(data['home_airports'], list) else data['home_airports']
        if 'preferred_airlines' in data:
            user.preferred_airlines = json.dumps(data['preferred_airlines']) if isinstance(data['preferred_airlines'], list) else data['preferred_airlines']
        if 'dietary_restrictions' in data:
            user.dietary_restrictions = data['dietary_restrictions']
        if 'travel_style' in data:
            user.travel_style = data['travel_style']
        if 'adults_count' in data:
            user.adults_count = int(data['adults_count'])
        if 'children_ages' in data:
            user.children_ages = json.dumps(data['children_ages']) if isinstance(data['children_ages'], list) else data['children_ages']
        if 'senior_travelers' in data:
            user.senior_travelers = bool(data['senior_travelers'])
        if 'preferred_accommodation' in data:
            user.preferred_accommodation = data['preferred_accommodation']
        
        db.session.commit()
        
        return jsonify({"message": "Profile updated successfully", "user": user.to_dict()})
        
    except Exception as exc:  # noqa: BLE001
        logging.exception("Error with profile API: %s", exc)
        db.session.rollback()
        return jsonify({"error": "Failed to process profile request"}), 500


@bp.route("/account")
@require_auth
def account():  # type: ignore[return-value]
    """Account settings page."""
    try:
        username = request.args.get('username', 'admin')
        user = User.query.filter_by(username=username).first()
        
        if not user:
            # Create default user if doesn't exist
            user = User(
                username=username,
                email=f"{username}@travelaigent.com",
                password_hash="temp_hash",
                first_name="",
                last_name="",
                adults_count=2,
                travel_style="luxury"
            )
            db.session.add(user)
            db.session.commit()
        
        return render_template("account.html", user=user)
    except Exception as exc:  # noqa: BLE001
        logging.exception("Error loading account: %s", exc)
        return render_template("error.html", message="Unable to load account"), 500


@bp.route("/api/user/preferences", methods=["GET", "PUT"])
@require_auth
def user_preferences():  # type: ignore[return-value]
    """API endpoint for user preferences."""
    try:
        username = request.args.get('username', 'admin')
        user = User.query.filter_by(username=username).first()
        
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        if request.method == "GET":
            # Parse preferences JSON
            prefs = json.loads(user.preferences) if user.preferences else {}
            return jsonify(prefs)
        
        # Handle PUT request
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Get existing preferences
        existing_prefs = json.loads(user.preferences) if user.preferences else {}
        
        # Update with new preferences
        existing_prefs.update(data)
        
        # Save back to user
        user.preferences = json.dumps(existing_prefs)
        db.session.commit()
        
        return jsonify({"message": "Preferences updated", "preferences": existing_prefs})
        
    except Exception as exc:  # noqa: BLE001
        logging.exception("Error with preferences API: %s", exc)
        return jsonify({"error": "Failed to process preferences"}), 500