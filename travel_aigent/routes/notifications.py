"""Routes for handling notifications and notification preferences."""
from flask import Blueprint, request, jsonify
from flask import current_app
import logging

from auth import require_auth
from ..models import db, Deal, User, TravelBrief
from ..services.notifications import notification_service

bp = Blueprint("notifications", __name__)


@bp.route("/api/notifications/send-pending")
@require_auth
def send_pending_notifications():
    """Send notifications for all pending deals."""
    try:
        # Get all deals that haven't been notified
        pending_deals = Deal.query.filter_by(
            notification_sent=False,
            status='active'
        ).filter(
            Deal.match_score >= 70  # Only notify for good matches
        ).all()
        
        sent_count = 0
        failed_count = 0
        
        for deal in pending_deals:
            try:
                # Get user and brief
                user = User.query.get(deal.user_id)
                brief = TravelBrief.query.get(deal.brief_id) if deal.brief_id else None
                
                if not user or not brief:
                    continue
                
                # Send notification
                results = notification_service.send_deal_notification(user, deal, brief)
                
                # Mark as sent if at least one channel succeeded
                if results['email'] or results['whatsapp']:
                    deal.notification_sent = True
                    db.session.commit()
                    sent_count += 1
                    logging.info(f"Notification sent for deal {deal.id} to user {user.username}")
                else:
                    failed_count += 1
                    logging.error(f"Failed to send notification for deal {deal.id}")
                    
            except Exception as e:
                logging.error(f"Error sending notification for deal {deal.id}: {e}")
                failed_count += 1
                continue
        
        return jsonify({
            "message": f"Notifications processed. Sent: {sent_count}, Failed: {failed_count}",
            "sent": sent_count,
            "failed": failed_count
        })
        
    except Exception as e:
        logging.error(f"Error processing notifications: {e}")
        return jsonify({"error": "Failed to process notifications"}), 500


@bp.route("/api/notifications/test", methods=["POST"])
@require_auth
def test_notification():
    """Test notification sending."""
    try:
        from auth import auth
        user = auth.get_current_user()
        
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        # Create test deal
        from datetime import datetime, timedelta
        test_deal = type('Deal', (), {
            'title': 'Test Deal: Paris Luxury Escape',
            'description': 'This is a test notification for your travel deals',
            'destination': 'Paris',
            'price': 1200,
            'original_price': 1500,
            'discount_percentage': 20,
            'departure_date': datetime.now() + timedelta(days=30),
            'return_date': datetime.now() + timedelta(days=37),
            'match_score': 95,
            'hotel_name': 'Test Hotel Paris',
            'hotel_rating': '5',
            'booking_url': 'https://travelaigent.com/deals'
        })()
        
        test_brief = type('Brief', (), {
            'departure_location': 'London',
            'destination': 'Paris'
        })()
        
        # Send test notification
        results = notification_service.send_deal_notification(user, test_deal, test_brief)
        
        return jsonify({
            "message": "Test notification sent",
            "results": results
        })
        
    except Exception as e:
        logging.error(f"Error sending test notification: {e}")
        return jsonify({"error": str(e)}), 500


@bp.route("/api/notifications/preferences", methods=["GET", "PUT"])
@require_auth
def notification_preferences():
    """Get or update notification preferences."""
    try:
        from auth import auth
        user = auth.get_current_user()
        
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        if request.method == "GET":
            # Get current preferences
            import json
            prefs = json.loads(user.preferences or '{}')
            return jsonify({
                "email_notifications": prefs.get('email_notifications', True),
                "whatsapp_notifications": prefs.get('whatsapp_notifications', False),
                "min_match_score": prefs.get('min_match_score', 70)
            })
        
        else:  # PUT
            data = request.get_json()
            import json
            
            # Update preferences
            prefs = json.loads(user.preferences or '{}')
            if 'email_notifications' in data:
                prefs['email_notifications'] = bool(data['email_notifications'])
            if 'whatsapp_notifications' in data:
                prefs['whatsapp_notifications'] = bool(data['whatsapp_notifications'])
            if 'min_match_score' in data:
                prefs['min_match_score'] = int(data['min_match_score'])
            
            user.preferences = json.dumps(prefs)
            db.session.commit()
            
            return jsonify({
                "message": "Preferences updated successfully",
                "preferences": prefs
            })
            
    except Exception as e:
        logging.error(f"Error handling notification preferences: {e}")
        return jsonify({"error": "Failed to handle preferences"}), 500