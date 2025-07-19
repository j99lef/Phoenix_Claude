"""Deals management routes"""
from flask import Blueprint, request, jsonify, session, render_template
from sqlalchemy import or_, and_
from datetime import datetime, timedelta
import logging

from ..models import db, Deal, User, TravelBrief
from auth import require_auth

bp = Blueprint("deals", __name__)


@bp.route("/deals")
@require_auth
def deals_list():
    """Display deals list page"""
    username = session.get('username', 'user')
    user = User.query.filter_by(username=username).first()
    return render_template("deals_list.html", user=user)


@bp.route("/api/deals")
@require_auth
def get_deals():
    """Get deals for the current user with filtering"""
    try:
        username = session.get('username', 'user')
        user = User.query.filter_by(username=username).first()
        
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        # Get query parameters
        status = request.args.get('status', 'active')
        destination = request.args.get('destination')
        min_price = request.args.get('min_price', type=float)
        max_price = request.args.get('max_price', type=float)
        deal_type = request.args.get('type')  # flight, hotel, package
        
        # Base query
        query = Deal.query.filter_by(user_id=user.id)
        
        # Apply filters
        if status:
            query = query.filter_by(status=status)
        if destination:
            query = query.filter(Deal.destination.ilike(f'%{destination}%'))
        if min_price:
            query = query.filter(Deal.price >= min_price)
        if max_price:
            query = query.filter(Deal.price <= max_price)
        if deal_type:
            query = query.filter_by(type=deal_type)
        
        # Order by match score and date
        deals = query.order_by(Deal.match_score.desc(), Deal.created_at.desc()).all()
        
        return jsonify([deal.to_dict() for deal in deals])
        
    except Exception as e:
        logging.error(f"Error fetching deals: {e}")
        return jsonify({"error": "Failed to fetch deals"}), 500


@bp.route("/api/deals/search")
@require_auth
def search_deals():
    """Search for new deals based on travel briefs"""
    try:
        username = session.get('username', 'user')
        user = User.query.filter_by(username=username).first()
        
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        # Get active briefs for the user
        active_briefs = TravelBrief.query.filter_by(
            user_id=user.id,
            status='active'
        ).all()
        
        if not active_briefs:
            return jsonify({
                "message": "No active travel briefs found",
                "deals_found": 0
            })
        
        # Import and use the travel agent to search for deals
        from travel_agent import TravelAgent
        agent = TravelAgent()
        
        total_deals = 0
        for brief in active_briefs:
            try:
                # Convert brief to dict format expected by travel agent
                brief_dict = {
                    'Brief_ID': brief.id,
                    'Destination': brief.destination,
                    'Travel_Dates': f"{brief.departure_date.strftime('%Y-%m-%d')} to {brief.return_date.strftime('%Y-%m-%d')}",
                    'Budget': brief.budget,
                    'Travelers': brief.travelers_count,
                    'Accommodation_Type': brief.accommodation_preferences
                }
                
                # Process the brief
                agent.process_brief(brief_dict)
                
                # Check for new deals in the database
                new_deals = Deal.query.filter_by(
                    brief_id=brief.id,
                    user_id=user.id,
                    notification_sent=False
                ).count()
                
                total_deals += new_deals
                
            except Exception as e:
                logging.error(f"Error processing brief {brief.id}: {e}")
                continue
        
        return jsonify({
            "message": f"Search complete. Found {total_deals} new deals.",
            "deals_found": total_deals,
            "briefs_processed": len(active_briefs)
        })
        
    except Exception as e:
        logging.error(f"Error searching deals: {e}")
        return jsonify({"error": "Failed to search for deals"}), 500


@bp.route("/api/deals/<int:deal_id>", methods=["PUT"])
@require_auth
def update_deal(deal_id):
    """Update deal status (e.g., mark as viewed, hidden, etc.)"""
    try:
        username = session.get('username', 'user')
        user = User.query.filter_by(username=username).first()
        
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        deal = Deal.query.filter_by(id=deal_id, user_id=user.id).first()
        if not deal:
            return jsonify({"error": "Deal not found"}), 404
        
        data = request.get_json()
        
        # Update allowed fields
        if 'status' in data:
            deal.status = data['status']
        if 'notification_sent' in data:
            deal.notification_sent = data['notification_sent']
        
        db.session.commit()
        return jsonify(deal.to_dict())
        
    except Exception as e:
        logging.error(f"Error updating deal: {e}")
        db.session.rollback()
        return jsonify({"error": "Failed to update deal"}), 500


@bp.route("/api/deals/recent")
def recent_deals():
    """Get recent deals across all users (for homepage)"""
    try:
        # Get recent active deals
        recent = Deal.query.filter_by(status='active').order_by(
            Deal.created_at.desc()
        ).limit(6).all()
        
        # Anonymize user data for privacy
        deals = []
        for deal in recent:
            deal_dict = deal.to_dict()
            # Remove user-specific data
            deal_dict.pop('user_id', None)
            deal_dict.pop('brief_id', None)
            deals.append(deal_dict)
        
        return jsonify(deals)
        
    except Exception as e:
        logging.error(f"Error fetching recent deals: {e}")
        return jsonify([])


@bp.route("/api/deals", methods=["POST"])
@require_auth
def create_deal():
    """Manually create a deal (for testing or manual additions)"""
    try:
        username = session.get('username', 'user')
        user = User.query.filter_by(username=username).first()
        
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        data = request.get_json()
        
        # Create new deal
        deal = Deal(
            user_id=user.id,
            brief_id=data.get('brief_id'),
            title=data.get('title', ''),
            description=data.get('description', ''),
            price=data.get('price', 0),
            original_price=data.get('original_price'),
            discount_percentage=data.get('discount_percentage', 0),
            provider=data.get('provider', 'Manual'),
            booking_url=data.get('booking_url', '#'),
            destination=data.get('destination', ''),
            departure_location=data.get('departure_location', ''),
            departure_date=datetime.fromisoformat(data['departure_date']) if data.get('departure_date') else None,
            return_date=datetime.fromisoformat(data['return_date']) if data.get('return_date') else None,
            accommodation_type=data.get('accommodation_type'),
            type=data.get('type', 'package'),
            hotel_name=data.get('hotel_name'),
            hotel_rating=data.get('hotel_rating'),
            airline=data.get('airline'),
            status='active',
            expires_at=datetime.now() + timedelta(days=7)
        )
        
        db.session.add(deal)
        db.session.commit()
        
        return jsonify(deal.to_dict()), 201
        
    except Exception as e:
        logging.error(f"Error creating deal: {e}")
        db.session.rollback()
        return jsonify({"error": "Failed to create deal"}), 500
