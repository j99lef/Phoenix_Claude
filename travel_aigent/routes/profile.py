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
        # Get current user
        from auth import auth
        user = auth.get_current_user()
        
        if not user:
            return redirect(url_for('auth.login'))
        
        return render_template("profile.html", user=user)
    except Exception as exc:  # noqa: BLE001
        logging.exception("Error loading profile: %s", exc)
        return render_template("error.html", message="Unable to load profile"), 500


@bp.route("/groups")
@require_auth
def travel_groups():  # type: ignore[return-value]
    """Travel groups management page."""
    try:
        # Get current user
        from auth import auth
        user = auth.get_current_user()
        
        if not user:
            return redirect(url_for('auth.login'))
        
        return render_template("groups.html", user=user)
    except Exception as exc:  # noqa: BLE001
        logging.exception("Error loading groups: %s", exc)
        return render_template("error.html", message="Unable to load groups"), 500


@bp.route("/api/profile", methods=["GET", "PUT"])
@require_auth
def api_profile():  # type: ignore[return-value]
    """API endpoint for profile data."""
    try:
        # Use the same method as other routes
        user = auth.get_current_user()
        
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        if request.method == "GET":
            return jsonify(user.to_dict())
        
        # Handle PUT request
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Update user fields
        updated_fields = []
        
        if 'first_name' in data:
            user.first_name = data['first_name']
            updated_fields.append('first_name')
        if 'last_name' in data:
            user.last_name = data['last_name']
            updated_fields.append('last_name')
        if 'email' in data:
            user.email = data['email']
            updated_fields.append('email')
        if 'phone' in data:
            user.phone = data['phone']
            updated_fields.append('phone')
        if 'whatsapp_number' in data:
            user.whatsapp_number = data['whatsapp_number']
            updated_fields.append('whatsapp_number')
        if 'home_airports' in data:
            user.home_airports = json.dumps(data['home_airports']) if isinstance(data['home_airports'], list) else data['home_airports']
            updated_fields.append('home_airports')
        if 'preferred_airlines' in data:
            user.preferred_airlines = json.dumps(data['preferred_airlines']) if isinstance(data['preferred_airlines'], list) else data['preferred_airlines']
            updated_fields.append('preferred_airlines')
        if 'dietary_restrictions' in data:
            user.dietary_restrictions = data['dietary_restrictions']
            updated_fields.append('dietary_restrictions')
        if 'travel_style' in data:
            user.travel_style = data['travel_style']
            updated_fields.append('travel_style')
        if 'adults_count' in data:
            user.adults_count = int(data['adults_count'])
            updated_fields.append('adults_count')
        if 'children_ages' in data:
            user.children_ages = json.dumps(data['children_ages']) if isinstance(data['children_ages'], list) else data['children_ages']
            updated_fields.append('children_ages')
        if 'senior_travelers' in data:
            user.senior_travelers = bool(data['senior_travelers'])
            updated_fields.append('senior_travelers')
        if 'preferred_accommodation' in data:
            user.preferred_accommodation = data['preferred_accommodation']
            updated_fields.append('preferred_accommodation')
        
        db.session.commit()
        
        logging.info(f"Updated profile for user {user.username} (ID: {user.id}). Fields updated: {', '.join(updated_fields)}")
        
        return jsonify({"message": "Profile updated successfully", "user": user.to_dict(), "updated_fields": updated_fields})
        
    except Exception as exc:  # noqa: BLE001
        logging.exception("Error with profile API: %s", exc)
        db.session.rollback()
        return jsonify({"error": "Failed to process profile request"}), 500


@bp.route("/account")
@require_auth
def account():  # type: ignore[return-value]
    """Account settings page."""
    try:
        from auth import auth
        user = auth.get_current_user()
        
        if not user:
            return redirect(url_for('auth.login'))
        
        return render_template("account.html", user=user)
    except Exception as exc:  # noqa: BLE001
        logging.exception("Error loading account: %s", exc)
        return render_template("error.html", message="Unable to load account"), 500


@bp.route("/api/user/preferences", methods=["GET", "PUT"])
@require_auth
def user_preferences():  # type: ignore[return-value]
    """API endpoint for user preferences."""
    try:
        # Use auth system consistently
        user = auth.get_current_user()
        
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