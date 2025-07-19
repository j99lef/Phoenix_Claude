"""Blueprint containing UI pages and brief/deal related API endpoints."""
from __future__ import annotations

import logging
import threading
from typing import Any, TypedDict

from flask import Blueprint, render_template, jsonify, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from travel_agent import TravelAgent
from validation import validate_and_sanitize_brief, validate_query_params, validate_brief_id
from auth import require_auth
from ..models import db, TravelBrief, Deal, User

# Rate limiter instance (will be initialized by app factory)
limiter = Limiter(key_func=get_remote_address)

bp = Blueprint("briefs", __name__)

_agent: TravelAgent | None = None


def _get_agent() -> TravelAgent:
    global _agent  # noqa: PLW0603
    if _agent is None:
        _agent = TravelAgent()
    return _agent


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------

@bp.route("/")
def index():  # type: ignore[return-value]
    """Main landing page - shows home for non-authenticated, dashboard for authenticated."""
    from flask import session
    
    # Check if user is authenticated
    if 'authenticated' in session and session['authenticated']:
        try:
            # Get current user
            from auth import auth
            user = auth.get_current_user()
            
            # Get stats for dashboard - filter by user
            if user and hasattr(user, 'id') and user.id > 0:
                # Regular user - filter by user_id
                briefs_count = TravelBrief.query.filter_by(user_id=user.id).count()
                recent_briefs = TravelBrief.query.filter_by(user_id=user.id).order_by(TravelBrief.created_at.desc()).limit(3).all()
            else:
                # Admin user or no valid user - show all briefs for now
                # TODO: Consider if admin should see all briefs or none
                briefs_count = 0
                recent_briefs = []
            
            return render_template("index.html", 
                                 briefs_count=briefs_count,
                                 recent_briefs=recent_briefs,
                                 user=user)
        except Exception as exc:  # noqa: BLE001
            logging.exception("Error loading dashboard: %s", exc)
            return render_template("index.html", briefs_count=0, recent_briefs=[], user=None)
    else:
        # Show home page for non-authenticated users
        return render_template("home.html")


@bp.route("/brief/<brief_id>")
@require_auth
def brief_detail(brief_id: str):  # type: ignore[return-value]
    """Detailed view of a specific travel brief with search activity."""
    from flask import session
    try:
        # Get current user
        from auth import auth
        user = auth.get_current_user()
        
        # Get brief from database
        brief = TravelBrief.query.get_or_404(brief_id)
        
        # Calculate search activity metrics
        from datetime import datetime, timezone
        now = datetime.now(timezone.utc)
        created_at = brief.created_at.replace(tzinfo=timezone.utc) if brief.created_at else now
        
        # Time since search started
        time_delta = now - created_at
        hours_active = max(1, int(time_delta.total_seconds() / 3600))
        days_active = max(1, time_delta.days)
        
        # Estimated scans (assuming scans every 30 minutes)
        estimated_scans = max(1, int(time_delta.total_seconds() / 1800))
        
        # Search activity status
        search_status = "Active" if time_delta.days < 30 else "Archived"
        
        # Check API health
        api_status = "Unknown"
        try:
            agent = _get_agent()
            if agent:
                if hasattr(agent, 'amadeus') and agent.amadeus:
                    api_status = "Active"
                elif hasattr(agent, 'sheets') and agent.sheets:
                    api_status = "Sheets Connected"
                else:
                    api_status = "Limited"
            else:
                api_status = "Offline"
        except Exception as e:
            logging.error(f"Error checking API status: {e}")
            api_status = "Error"

        activity_stats = {
            'hours_active': hours_active,
            'days_active': days_active,
            'estimated_scans': estimated_scans,
            'search_status': search_status,
            'created_at': created_at,
            'api_status': api_status
        }
        
        return render_template("brief_detail.html", brief=brief, activity_stats=activity_stats, user=user)
    except Exception as exc:  # noqa: BLE001
        logging.exception("Error loading brief detail for %s", brief_id)
        return render_template("error.html", message="Unable to load brief details"), 500


@bp.route("/brief/new")
@require_auth
def new_brief():  # type: ignore[return-value]
    """Create a new travel brief."""
    from flask import session
    from auth import auth
    user = auth.get_current_user()
    return render_template("brief_form.html", brief=None, mode="create", user=user)


@bp.route("/briefs")
@require_auth
def briefs_list():  # type: ignore[return-value]
    """List all travel briefs."""
    from flask import session
    try:
        # Get current user properly
        from auth import auth
        user = auth.get_current_user()
        
        # Get briefs for the current user
        if user and hasattr(user, 'id') and user.id > 0:
            briefs = TravelBrief.query.filter_by(user_id=user.id).order_by(TravelBrief.created_at.desc()).all()
        else:
            # Admin or invalid user - show no briefs
            briefs = []
            
        return render_template("briefs_list.html", briefs=briefs, user=user)
    except Exception as exc:  # noqa: BLE001
        logging.exception("Error loading briefs list: %s", exc)
        return render_template("error.html", message="Unable to load briefs"), 500


@bp.route("/deals")
@require_auth
def deals_list():  # type: ignore[return-value]
    """List travel deals."""
    from flask import session
    try:
        username = session.get('username', 'user')
        user = User.query.filter_by(username=username).first()
        return render_template("deals_list.html", user=user)
    except Exception as exc:  # noqa: BLE001
        logging.exception("Error loading deals: %s", exc)
        return render_template("error.html", message="Unable to load deals"), 500


@bp.route("/brief/<brief_id>/edit")
@require_auth
def edit_brief(brief_id: str):  # type: ignore[return-value]
    """Edit an existing travel brief."""
    from flask import session
    try:
        username = session.get('username', 'user')
        user = User.query.filter_by(username=username).first()
        # Get brief from database, not Google Sheets
        brief = TravelBrief.query.get_or_404(brief_id)
        return render_template("brief_form.html", brief=brief, mode="edit", user=user)
    except Exception as exc:  # noqa: BLE001
        logging.exception("Error loading brief for editing: %s", brief_id)
        return render_template("error.html", message="Error loading brief"), 500


# ---------------------------------------------------------------------------
# JSON API endpoints
# ---------------------------------------------------------------------------

@bp.route("/api/briefs")
@require_auth
def get_briefs():  # type: ignore[return-value]
    try:
        # Get current user
        from auth import auth
        user = auth.get_current_user()
        
        # Get briefs from database filtered by user
        if user and hasattr(user, 'id') and user.id > 0:
            briefs = TravelBrief.query.filter_by(user_id=user.id).order_by(TravelBrief.created_at.desc()).all()
        else:
            briefs = []
            
        briefs_data = [brief.to_dict() for brief in briefs]
        return jsonify(briefs_data)
    except Exception as exc:  # noqa: BLE001
        logging.exception("Error fetching briefs: %s", exc)
        return jsonify([]), 200


class _Deal(TypedDict):
    ai_score: int | float | str | None


@bp.route("/api/deals")
def get_recent_deals():  # type: ignore[return-value]
    try:
        # Validate query parameters
        try:
            validated_params = validate_query_params(request.args.to_dict())
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
            
        min_score = validated_params["min_score"]
        max_price = validated_params["max_price"] 
        destination = validated_params["destination"].lower()
        limit = validated_params["limit"]
        
        # First try to get deals from database
        from ..models import Deal
        db_deals = Deal.query.all()
        
        if db_deals:
            # Use database deals
            qualified = []
            for deal in db_deals:
                # Apply filters
                if deal.total_price and deal.total_price > max_price:
                    continue
                if destination and destination not in deal.destination.lower():
                    continue
                
                # Convert to dict format expected by frontend
                deal_dict = {
                    'id': deal.id,
                    'destination': deal.destination,
                    'destination_name': deal.destination,
                    'total_price': deal.total_price or deal.price,
                    'departure_date': deal.departure_date.isoformat() if deal.departure_date else None,
                    'return_date': deal.return_date.isoformat() if deal.return_date else None,
                    'airline': deal.airline,
                    'hotel_name': deal.hotel_name,
                    'hotel_rating': deal.hotel_rating,
                    'ai_score': 8.5,  # Default score
                    'booking_url': deal.booking_url,
                    'provider': deal.provider,
                    'type': deal.type
                }
                qualified.append(deal_dict)
            
            return jsonify(qualified[:limit])
        
        # Fallback to sheets if available
        agent = _get_agent()
        if agent and hasattr(agent, 'sheets') and agent.sheets:
            all_deals: list[_Deal] = agent.sheets.get_recent_deals(limit=50)
            qualified: list[_Deal] = []
        
        for deal in all_deals:
            try:
                # Score filtering
                score_raw = deal.get("ai_score", 0)
                if isinstance(score_raw, str):
                    if "/" in score_raw:
                        score_raw = score_raw.split("/")[0]
                    if score_raw in {"N/A", "NaN", "", "None"}:
                        continue
                score_val = float(score_raw or 0)
                if score_val < min_score:
                    continue
                    
                # Price filtering
                price_raw = deal.get("total_price") or deal.get("Total_Price", 0)
                price_val = float(price_raw or 0)
                if price_val > max_price:
                    continue
                    
                # Destination filtering
                if destination:
                    deal_dest = (deal.get("destination") or deal.get("Destination", "")).lower()
                    if destination not in deal_dest:
                        continue
                
                # Add booking URL if not present
                if not deal.get("booking_url"):
                    dest_code = deal.get("destination") or deal.get("Destination", "")
                    deal["booking_url"] = f"https://www.skyscanner.com/transport/flights/lon/{dest_code.lower()[:3]}/"
                    deal["provider"] = "Skyscanner"
                
                qualified.append(deal)
            except (ValueError, TypeError):
                continue
                
        # Sort by AI score (highest first)
        qualified.sort(key=lambda x: float(x.get("ai_score", 0) or 0), reverse=True)
        return jsonify(qualified[:limit])
    except Exception as exc:  # noqa: BLE001
        logging.exception("Error fetching deals: %s", exc)
        return jsonify({"error": "Unable to fetch deals"}), 500


# ---------------------------------------------------------------------------
# Actions
# ---------------------------------------------------------------------------

@bp.route("/api/run-search", methods=["POST"])
@limiter.limit("5 per minute")
def manual_search():  # type: ignore[return-value]
    agent = _get_agent()

    def _run():
        if agent:
            agent.run_deal_search()

    threading.Thread(target=_run, daemon=True).start()
    return jsonify({"message": "Search started"})


@bp.route("/api/test-notification", methods=["POST"])
def test_notification():  # type: ignore[return-value]
    agent = _get_agent()
    try:
        test_deal = {
            "type": "flight",
            "destination": "PAR",
            "departure_date": "2025-08-15",
            "total_price": 450.0,
            "currency": "GBP",
            "airline": "BA",
        }
        test_analysis = {
            "score": 9,
            "recommendation": "BOOK_NOW",
            "action_summary": "This is a test notification from Travel AiGent",
        }
        test_brief = {"Brief_ID": "TEST", "Destinations": "Paris"}

        if agent and agent.telegram:
            agent.telegram.send_alert(test_deal, test_analysis, test_brief)  # type: ignore[arg-type]
        else:
            logging.info("Mock notification: would send Telegram alert")
        return jsonify({"message": "Test notification executed"})
    except Exception as exc:  # noqa: BLE001
        logging.exception("Test notification error: %s", exc)
        return jsonify({"message": "Error"}), 200


@bp.route("/api/briefs", methods=["POST"])
@limiter.limit("10 per hour")
@require_auth
def create_brief():  # type: ignore[return-value]
    """Create a new travel brief."""
    agent = _get_agent()
    try:
        # Get current user
        from auth import auth
        user = auth.get_current_user()
        if not user or not hasattr(user, 'id') or user.id == 0:
            return jsonify({"error": "Valid user required to create briefs"}), 403
        
        # Get and validate JSON data
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Validate and sanitize input data
        try:
            validated_data = validate_and_sanitize_brief(data)
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        
        # Generate a new brief ID
        import time
        brief_id = f"TB-{int(time.time())}"
        
        # Create new travel brief in database
        from datetime import datetime
        
        # Parse travel dates if provided
        departure_date = None
        return_date = None
        try:
            if 'departure_date' in validated_data and validated_data['departure_date']:
                departure_date = datetime.strptime(validated_data['departure_date'], '%Y-%m-%d')
            if 'return_date' in validated_data and validated_data['return_date']:
                return_date = datetime.strptime(validated_data['return_date'], '%Y-%m-%d')
        except:
            departure_date = datetime.now()
        
        # Create database record
        new_brief = TravelBrief(
            user_id=user.id,  # Associate with current user
            departure_location=validated_data["departure_location"],
            destination=validated_data["destinations"],
            departure_date=departure_date,
            return_date=return_date,
            travelers=validated_data["travelers"],
            budget_min=validated_data["budget_min"],
            budget_max=validated_data["budget_max"],
            accommodation_type=validated_data["accommodation_type"],
            interests=validated_data.get("ai_instructions", ""),
            trip_length=7.0,  # Default trip length
            date_flexibility=validated_data.get("date_flexibility", 2)  # Default 2 days flexibility
        )
        
        # Save to database
        db.session.add(new_brief)
        db.session.commit()
        
        logging.info(f"Successfully created travel brief with ID: {new_brief.id}")
        
        # Trigger deal search for this brief
        try:
            agent = _get_agent()
            if agent:
                # Convert database brief to format expected by travel agent
                brief_dict = {
                    'Brief_ID': str(new_brief.id),
                    'Departure_Location': new_brief.departure_location,
                    'Destinations': new_brief.destination,
                    'Travelers': new_brief.travelers,
                    'Budget_Min': new_brief.budget_min,
                    'Budget_Max': new_brief.budget_max,
                    'Accommodation_Type': new_brief.accommodation_type,
                    'AI_Instructions': new_brief.interests,
                    'Trip_Duration': f"{new_brief.trip_length} days"
                }
                
                # Start deal search in background
                import threading
                def search_deals():
                    try:
                        agent.process_travel_brief(brief_dict)
                    except Exception as e:
                        logging.error(f"Error in background deal search: {e}")
                
                threading.Thread(target=search_deals, daemon=True).start()
                logging.info(f"Started deal search for brief {new_brief.id}")
        except Exception as e:
            logging.error(f"Error starting deal search: {e}")
        
        return jsonify({"message": "Travel brief created successfully! Deal search started.", "brief_id": new_brief.id})
        
    except Exception as exc:  # noqa: BLE001
        logging.exception("Error creating brief: %s", exc)
        return jsonify({"error": "Failed to create brief"}), 500


@bp.route("/api/briefs/<int:brief_id>/deals")
def get_brief_deals(brief_id: int):  # type: ignore[return-value]
    """Get deals for a specific brief."""
    try:
        # Check if brief exists
        brief = TravelBrief.query.get(brief_id)
        if not brief:
            return jsonify({"error": "Brief not found"}), 404
        
        # Get deals for this brief
        deals = Deal.query.filter_by(brief_id=brief_id).order_by(Deal.created_at.desc()).all()
        
        # Convert to JSON
        deals_data = []
        for deal in deals:
            deal_dict = deal.to_dict()
            # Add destination name if available
            if deal.destination:
                destinations = {
                    'BCN': 'Barcelona',
                    'VAL': 'Valencia', 
                    'VLC': 'Valencia',
                    'FCO': 'Rome',
                    'ROM': 'Rome',
                    'ATH': 'Athens',
                    'LCA': 'Cyprus',
                    'LIS': 'Lisbon',
                    'MAD': 'Madrid',
                    'PMI': 'Mallorca',
                    'CDG': 'Paris',
                    'DXB': 'Dubai',
                    'JFK': 'New York',
                    'AMS': 'Amsterdam'
                }
                deal_dict['destination_name'] = destinations.get(deal.destination, deal.destination)
            deals_data.append(deal_dict)
        
        return jsonify(deals_data)
        
    except Exception as exc:  # noqa: BLE001
        logging.exception("Error fetching deals for brief %s", brief_id)
        return jsonify({"error": "Failed to fetch deals"}), 500


@bp.route("/api/briefs/<brief_id>", methods=["PUT"])
def update_brief(brief_id: str):  # type: ignore[return-value]
    """Update an existing travel brief."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Validate and sanitize input data
        try:
            validated_data = validate_and_sanitize_brief(data)
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        
        # Find existing brief in database
        brief = TravelBrief.query.get(brief_id)
        if not brief:
            return jsonify({"error": "Brief not found"}), 404
        
        # Update brief fields
        brief.departure_location = validated_data["departure_location"]
        brief.destination = validated_data["destinations"]
        brief.travelers = validated_data["travelers"]
        brief.budget_min = validated_data["budget_min"]
        brief.budget_max = validated_data["budget_max"]
        brief.accommodation_type = validated_data["accommodation_type"]
        brief.interests = validated_data.get("ai_instructions", "")
        brief.date_flexibility = validated_data.get("date_flexibility", 2)
        
        # Parse travel dates if provided - for now use existing dates
        from datetime import datetime
        brief.updated_at = datetime.utcnow()
        
        # Save to database
        db.session.commit()
        
        logging.info(f"Successfully updated travel brief with ID: {brief.id}")
        return jsonify({"message": "Travel brief updated successfully!", "brief_id": brief.id})
        
    except Exception as exc:  # noqa: BLE001
        logging.exception("Error updating brief: %s", exc)
        return jsonify({"error": "Failed to update brief"}), 500


@bp.route("/api/briefs/<brief_id>", methods=["DELETE"])
def delete_brief(brief_id: str):  # type: ignore[return-value]
    """Delete a travel brief."""
    try:
        # Find brief in database
        brief = TravelBrief.query.get(brief_id)
        if not brief:
            return jsonify({"error": "Brief not found"}), 404
        
        # Delete from database
        db.session.delete(brief)
        db.session.commit()
        
        logging.info(f"Successfully deleted travel brief with ID: {brief_id}")
        return jsonify({"message": "Brief deleted successfully"})
        
    except Exception as exc:  # noqa: BLE001
        logging.exception("Error deleting brief: %s", exc)
        return jsonify({"error": "Failed to delete brief"}), 500


# Booking functionality removed - TravelAiGent is a deal finder that redirects to external partners


@bp.route("/api/briefs/<brief_id>/status", methods=["PUT"])
def update_brief_status(brief_id: str):  # type: ignore[return-value]
    """Update the status of a travel brief."""
    try:
        data = request.get_json()
        if not data or 'status' not in data:
            return jsonify({"error": "Status is required"}), 400
        
        # Validate status
        valid_statuses = ['active', 'paused', 'completed', 'cancelled']
        new_status = data['status']
        if new_status not in valid_statuses:
            return jsonify({"error": "Invalid status"}), 400
        
        # Find brief in database
        brief = TravelBrief.query.get(brief_id)
        if not brief:
            return jsonify({"error": "Brief not found"}), 404
        
        # Update status
        brief.status = new_status
        from datetime import datetime
        brief.updated_at = datetime.utcnow()
        
        # Save to database
        db.session.commit()
        
        logging.info(f"Successfully updated brief {brief_id} status to {new_status}")
        return jsonify({"message": "Brief status updated successfully", "status": new_status})
        
    except Exception as exc:  # noqa: BLE001
        logging.exception("Error updating brief status: %s", exc)
        return jsonify({"error": "Failed to update brief status"}), 500
