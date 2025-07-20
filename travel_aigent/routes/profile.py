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
            logging.error("No user found for profile page")
            return redirect(url_for('auth.login'))
        
        logging.info(f"Loading profile page for user: {user.username} (ID: {user.id if hasattr(user, 'id') else 'No ID'})")
        
        # Make sure user has all required attributes with safe defaults
        if not hasattr(user, 'first_name'):
            user.first_name = ''
        if not hasattr(user, 'last_name'):
            user.last_name = ''
        if not hasattr(user, 'email'):
            user.email = ''
        if not hasattr(user, 'phone'):
            user.phone = ''
        if not hasattr(user, 'whatsapp_number'):
            user.whatsapp_number = ''
        if not hasattr(user, 'home_airports'):
            user.home_airports = ''
        if not hasattr(user, 'preferred_airlines'):
            user.preferred_airlines = ''
        if not hasattr(user, 'dietary_restrictions'):
            user.dietary_restrictions = ''
        if not hasattr(user, 'travel_style'):
            user.travel_style = 'comfort'  # Default value
        if not hasattr(user, 'adults_count'):
            user.adults_count = 2
        if not hasattr(user, 'children_ages'):
            user.children_ages = ''
        if not hasattr(user, 'senior_travelers'):
            user.senior_travelers = False
        if not hasattr(user, 'preferred_accommodation'):
            user.preferred_accommodation = ''
            
        # Log what we're sending to template
        logging.info(f"User attributes: first_name={user.first_name}, email={user.email}, travel_style={user.travel_style}")
            
        # Use production-ready profile template
        return render_template("profile_production.html", user=user)
    except Exception as exc:  # noqa: BLE001
        logging.exception("Error loading profile: %s", exc)
        # Return a more detailed error for debugging
        error_details = f"Error: {str(exc)} (Type: {type(exc).__name__})"
        return render_template("error.html", message=error_details), 500


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


@bp.route("/profile/simple")
@require_auth
def profile_simple():  # type: ignore[return-value]
    """Simple profile page for debugging."""
    try:
        from auth import auth
        user = auth.get_current_user()
        
        if not user:
            logging.error("No user found for simple profile page")
            return redirect(url_for('auth.login'))
            
        return render_template("profile_simple.html", user=user)
    except Exception as exc:  # noqa: BLE001
        logging.exception("Error loading simple profile: %s", exc)
        return jsonify({"error": str(exc), "type": str(type(exc))}), 500


@bp.route("/profile/original")
@require_auth
def profile_original():  # type: ignore[return-value]
    """Original profile page (might have issues)."""
    try:
        from auth import auth
        user = auth.get_current_user()
        
        if not user:
            return redirect(url_for('auth.login'))
            
        # Make sure user has all required attributes with safe defaults
        if not hasattr(user, 'first_name'):
            user.first_name = ''
        if not hasattr(user, 'last_name'):
            user.last_name = ''
        if not hasattr(user, 'email'):
            user.email = ''
        if not hasattr(user, 'phone'):
            user.phone = ''
        if not hasattr(user, 'whatsapp_number'):
            user.whatsapp_number = ''
        if not hasattr(user, 'home_airports'):
            user.home_airports = ''
        if not hasattr(user, 'preferred_airlines'):
            user.preferred_airlines = ''
        if not hasattr(user, 'dietary_restrictions'):
            user.dietary_restrictions = ''
        if not hasattr(user, 'travel_style'):
            user.travel_style = 'comfort'
        if not hasattr(user, 'adults_count'):
            user.adults_count = 2
        if not hasattr(user, 'children_ages'):
            user.children_ages = ''
        if not hasattr(user, 'senior_travelers'):
            user.senior_travelers = False
        if not hasattr(user, 'preferred_accommodation'):
            user.preferred_accommodation = ''
            
        return render_template("profile.html", user=user)
    except Exception as exc:  # noqa: BLE001
        logging.exception("Error loading original profile: %s", exc)
        return jsonify({"error": str(exc), "type": str(type(exc))}), 500


@bp.route("/profile/debug")
@require_auth
def profile_debug():  # type: ignore[return-value]
    """Debug endpoint to check profile functionality."""
    try:
        from auth import auth
        user = auth.get_current_user()
        
        debug_info = {
            "authenticated": auth.is_authenticated(),
            "session_username": session.get('username'),
            "user_found": user is not None,
        }
        
        if user:
            debug_info.update({
                "user_id": getattr(user, 'id', 'No ID'),
                "username": getattr(user, 'username', 'No username'),
                "first_name": getattr(user, 'first_name', 'No first_name'),
                "last_name": getattr(user, 'last_name', 'No last_name'),
                "email": getattr(user, 'email', 'No email'),
                "has_attributes": {
                    "id": hasattr(user, 'id'),
                    "username": hasattr(user, 'username'),
                    "first_name": hasattr(user, 'first_name'),
                    "last_name": hasattr(user, 'last_name'),
                    "email": hasattr(user, 'email'),
                }
            })
        
        return jsonify(debug_info)
    except Exception as e:
        return jsonify({"error": str(e), "type": str(type(e))}), 500


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