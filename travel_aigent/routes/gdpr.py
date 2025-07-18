"""GDPR compliance routes for TravelAiGent"""
from flask import Blueprint, request, jsonify, session, send_file
from auth import require_auth
from ..models import db, User
from ..gdpr import GDPRCompliance
import json
import io
from datetime import datetime

bp = Blueprint("gdpr", __name__)


@bp.route("/api/gdpr/export")
@require_auth
def export_user_data():
    """Export all user data in JSON format (GDPR Article 20 - Data Portability)"""
    try:
        username = session.get('username', 'admin')
        user = User.query.filter_by(username=username).first()
        
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        # Get all user data
        user_data = GDPRCompliance.export_user_data(user.id)
        
        # Create downloadable JSON file
        json_data = json.dumps(user_data, indent=2)
        buffer = io.BytesIO()
        buffer.write(json_data.encode('utf-8'))
        buffer.seek(0)
        
        filename = f"travelaigent_data_export_{username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        return send_file(
            buffer,
            mimetype='application/json',
            as_attachment=True,
            download_name=filename
        )
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route("/api/gdpr/delete", methods=["POST"])
@require_auth
def delete_user_data():
    """Delete user data (GDPR Article 17 - Right to Erasure)"""
    try:
        username = session.get('username', 'admin')
        user = User.query.filter_by(username=username).first()
        
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        data = request.get_json() or {}
        delete_account = data.get('delete_account', False)
        
        # Confirm deletion with password
        password = data.get('password')
        if not password:
            return jsonify({"error": "Password required for data deletion"}), 400
        
        # Verify password
        from auth import auth
        if not auth.authenticate(username, password):
            return jsonify({"error": "Invalid password"}), 401
        
        # Delete user data
        result = GDPRCompliance.delete_user_data(user.id, delete_account)
        
        if result.get("success"):
            if delete_account:
                # Log out user after account deletion
                session.clear()
            return jsonify(result)
        else:
            return jsonify(result), 500
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route("/api/gdpr/consent", methods=["GET", "PUT"])
@require_auth
def manage_consent():
    """Get or update consent preferences"""
    try:
        username = session.get('username', 'admin')
        user = User.query.filter_by(username=username).first()
        
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        if request.method == "GET":
            # Get current consent status
            consent_status = GDPRCompliance.get_consent_status(user.id)
            return jsonify(consent_status)
        
        else:  # PUT
            # Update consent preferences
            consent_data = request.get_json() or {}
            consent_data['ip_address'] = request.remote_addr
            
            result = GDPRCompliance.update_consent(user.id, consent_data)
            
            if result.get("success"):
                return jsonify(result)
            else:
                return jsonify(result), 500
                
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route("/privacy-policy")
def privacy_policy():
    """Privacy policy page"""
    from flask import render_template
    return render_template("privacy_policy.html")


@bp.route("/cookie-policy")
def cookie_policy():
    """Cookie policy page"""
    from flask import render_template
    return render_template("cookie_policy.html")