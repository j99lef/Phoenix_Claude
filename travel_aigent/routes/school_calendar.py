"""School calendar routes for managing UK school holidays and inset days"""
from flask import Blueprint, request, jsonify, render_template
from datetime import datetime
import logging

from ..models import db, UserSchoolCalendar, InsetDay
from auth import require_auth, auth
from uk_school_holidays import UK_SCHOOL_HOLIDAYS, HOLIDAY_TYPES, get_holidays_for_country, get_upcoming_holidays

bp = Blueprint("school_calendar", __name__)


@bp.route("/api/school-calendar", methods=["GET"])
@require_auth
def get_school_calendar():
    """Get user's school calendar settings"""
    try:
        user = auth.get_current_user()
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        # Get or create calendar
        calendar = UserSchoolCalendar.query.filter_by(user_id=user.id).first()
        
        if not calendar:
            return jsonify({
                "country": None,
                "inset_days": [],
                "holidays": []
            })
        
        # Get holidays for the country
        holidays = get_holidays_for_country(calendar.country)
        
        return jsonify({
            "country": calendar.country,
            "inset_days": [day.to_dict() for day in calendar.inset_days],
            "holidays": holidays
        })
        
    except Exception as e:
        logging.error(f"Error getting school calendar: {e}")
        return jsonify({"error": "Failed to get school calendar"}), 500


@bp.route("/api/school-calendar", methods=["POST"])
@require_auth
def update_school_calendar():
    """Update user's school calendar settings"""
    try:
        user = auth.get_current_user()
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        data = request.get_json()
        country = data.get("country")
        
        if country not in ["England", "Scotland", "Wales", "Northern Ireland"]:
            return jsonify({"error": "Invalid country"}), 400
        
        # Get or create calendar
        calendar = UserSchoolCalendar.query.filter_by(user_id=user.id).first()
        
        if not calendar:
            calendar = UserSchoolCalendar(
                user_id=user.id,
                country=country
            )
            db.session.add(calendar)
        else:
            calendar.country = country
            calendar.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify(calendar.to_dict())
        
    except Exception as e:
        logging.error(f"Error updating school calendar: {e}")
        db.session.rollback()
        return jsonify({"error": "Failed to update school calendar"}), 500


@bp.route("/api/school-calendar/inset-days", methods=["POST"])
@require_auth
def add_inset_day():
    """Add an inset day to user's calendar"""
    try:
        user = auth.get_current_user()
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        # Get calendar
        calendar = UserSchoolCalendar.query.filter_by(user_id=user.id).first()
        if not calendar:
            return jsonify({"error": "School calendar not configured"}), 400
        
        data = request.get_json()
        date_str = data.get("date")
        description = data.get("description", "")
        
        if not date_str:
            return jsonify({"error": "Date is required"}), 400
        
        # Parse date
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return jsonify({"error": "Invalid date format"}), 400
        
        # Check if date already exists
        existing = InsetDay.query.filter_by(
            calendar_id=calendar.id,
            date=date
        ).first()
        
        if existing:
            return jsonify({"error": "Inset day already exists for this date"}), 400
        
        # Create inset day
        inset_day = InsetDay(
            calendar_id=calendar.id,
            date=date,
            description=description
        )
        
        db.session.add(inset_day)
        db.session.commit()
        
        return jsonify(inset_day.to_dict()), 201
        
    except Exception as e:
        logging.error(f"Error adding inset day: {e}")
        db.session.rollback()
        return jsonify({"error": "Failed to add inset day"}), 500


@bp.route("/api/school-calendar/inset-days/<int:day_id>", methods=["DELETE"])
@require_auth
def delete_inset_day(day_id):
    """Delete an inset day"""
    try:
        user = auth.get_current_user()
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        # Get calendar
        calendar = UserSchoolCalendar.query.filter_by(user_id=user.id).first()
        if not calendar:
            return jsonify({"error": "School calendar not configured"}), 400
        
        # Get inset day
        inset_day = InsetDay.query.filter_by(
            id=day_id,
            calendar_id=calendar.id
        ).first()
        
        if not inset_day:
            return jsonify({"error": "Inset day not found"}), 404
        
        db.session.delete(inset_day)
        db.session.commit()
        
        return jsonify({"message": "Inset day deleted"}), 200
        
    except Exception as e:
        logging.error(f"Error deleting inset day: {e}")
        db.session.rollback()
        return jsonify({"error": "Failed to delete inset day"}), 500


@bp.route("/api/school-holidays/<country>")
def get_country_holidays(country):
    """Get school holidays for a specific country"""
    try:
        if country not in ["England", "Scotland", "Wales", "Northern-Ireland"]:
            return jsonify({"error": "Invalid country"}), 400
        
        # Convert URL format to data format
        country_key = country.replace("-", " ")
        
        holidays = get_holidays_for_country(country_key)
        
        return jsonify({
            "country": country_key,
            "holidays": holidays,
            "holiday_types": HOLIDAY_TYPES
        })
        
    except Exception as e:
        logging.error(f"Error getting holidays: {e}")
        return jsonify({"error": "Failed to get holidays"}), 500


@bp.route("/api/school-holidays/upcoming")
@require_auth
def get_upcoming_school_holidays():
    """Get upcoming holidays based on user's calendar"""
    try:
        user = auth.get_current_user()
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        # Get calendar
        calendar = UserSchoolCalendar.query.filter_by(user_id=user.id).first()
        if not calendar:
            return jsonify({
                "message": "Please configure your school calendar in your profile",
                "holidays": []
            })
        
        # Get upcoming holidays
        holidays = get_upcoming_holidays(calendar.country)
        
        # Add inset days
        upcoming_inset_days = []
        today = datetime.now().date()
        
        for inset_day in calendar.inset_days:
            if inset_day.date >= today:
                upcoming_inset_days.append({
                    "name": f"Inset Day - {inset_day.description or 'School Closed'}",
                    "start": inset_day.date.isoformat(),
                    "end": inset_day.date.isoformat(),
                    "type": "inset_day"
                })
        
        # Combine and sort
        all_holidays = holidays + upcoming_inset_days
        all_holidays.sort(key=lambda x: x["start"])
        
        return jsonify({
            "country": calendar.country,
            "holidays": all_holidays[:10]  # Return next 10 holidays
        })
        
    except Exception as e:
        logging.error(f"Error getting upcoming holidays: {e}")
        return jsonify({"error": "Failed to get upcoming holidays"}), 500