"""GDPR compliance utilities for TravelAiGent"""
import json
import logging
from datetime import datetime
from typing import Dict, Any
from flask import jsonify
from .models import db, User, TravelBrief, TravelGroup, UserSchool, Deal


class GDPRCompliance:
    """Handle GDPR compliance requirements"""
    
    @staticmethod
    def export_user_data(user_id: int) -> Dict[str, Any]:
        """Export all user data for GDPR data portability"""
        try:
            user = User.query.get(user_id)
            if not user:
                return {"error": "User not found"}
            
            # Collect all user data
            user_data = {
                "profile": {
                    "username": user.username,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "phone": user.phone,
                    "created_at": user.created_at.isoformat() if user.created_at else None,
                    "last_login": user.last_login.isoformat() if user.last_login else None
                },
                "preferences": json.loads(user.preferences) if user.preferences else {},
                "travel_settings": {
                    "home_airports": json.loads(user.home_airports) if user.home_airports else [],
                    "preferred_airlines": json.loads(user.preferred_airlines) if user.preferred_airlines else [],
                    "dietary_restrictions": user.dietary_restrictions,
                    "travel_style": user.travel_style,
                    "preferred_accommodation": user.preferred_accommodation,
                    "adults_count": user.adults_count,
                    "children_ages": json.loads(user.children_ages) if user.children_ages else [],
                    "senior_travelers": user.senior_travelers
                },
                "travel_briefs": [
                    {
                        "id": brief.id,
                        "destination": brief.destination,
                        "departure_location": brief.departure_location,
                        "departure_date": brief.departure_date.isoformat() if brief.departure_date else None,
                        "return_date": brief.return_date.isoformat() if brief.return_date else None,
                        "travelers": brief.travelers,
                        "budget_min": brief.budget_min,
                        "budget_max": brief.budget_max,
                        "interests": brief.interests,
                        "created_at": brief.created_at.isoformat() if brief.created_at else None
                    }
                    for brief in user.travel_briefs
                ],
                "travel_groups": [
                    {
                        "id": group.id,
                        "group_name": group.group_name,
                        "group_type": group.group_type,
                        "members": json.loads(group.members) if group.members else [],
                        "created_at": group.created_at.isoformat() if group.created_at else None
                    }
                    for group in user.travel_groups
                ],
                "schools": [
                    {
                        "school_name": school.school_name,
                        "school_type": school.school_type,
                        "region": school.region,
                        "country": school.country,
                        "child_name": school.child_name,
                        "is_primary": school.is_primary
                    }
                    for school in user.schools
                ],
                "export_date": datetime.now().isoformat(),
                "export_format_version": "1.0"
            }
            
            return user_data
            
        except Exception as e:
            logging.error(f"Error exporting user data: {e}")
            return {"error": str(e)}
    
    @staticmethod
    def delete_user_data(user_id: int, delete_account: bool = False) -> Dict[str, Any]:
        """Delete user data for GDPR right to erasure"""
        try:
            user = User.query.get(user_id)
            if not user:
                return {"error": "User not found"}
            
            # Delete associated data
            deleted_counts = {
                "travel_briefs": 0,
                "travel_groups": 0,
                "schools": 0,
                "deals": 0
            }
            
            # Delete travel briefs
            for brief in user.travel_briefs:
                # Delete associated deals first
                Deal.query.filter_by(brief_id=brief.id).delete()
                deleted_counts["deals"] += db.session.query(Deal).filter_by(brief_id=brief.id).count()
                db.session.delete(brief)
                deleted_counts["travel_briefs"] += 1
            
            # Delete travel groups
            for group in user.travel_groups:
                db.session.delete(group)
                deleted_counts["travel_groups"] += 1
            
            # Delete schools
            for school in user.schools:
                db.session.delete(school)
                deleted_counts["schools"] += 1
            
            if delete_account:
                # Anonymize user data instead of hard delete
                user.username = f"deleted_user_{user.id}"
                user.email = f"deleted_{user.id}@example.com"
                user.first_name = "Deleted"
                user.last_name = "User"
                user.phone = None
                user.home_airports = None
                user.preferred_airlines = None
                user.dietary_restrictions = None
                user.preferences = json.dumps({"deleted": True})
                user.password_hash = "DELETED"
                deleted_counts["account"] = "anonymized"
            else:
                # Just clear personal data
                user.phone = None
                user.dietary_restrictions = None
                user.preferences = json.dumps({"email_notifications": False})
            
            db.session.commit()
            
            return {
                "success": True,
                "deleted": deleted_counts,
                "message": "User data deleted successfully"
            }
            
        except Exception as e:
            logging.error(f"Error deleting user data: {e}")
            db.session.rollback()
            return {"error": str(e)}
    
    @staticmethod
    def get_consent_status(user_id: int) -> Dict[str, Any]:
        """Get user's consent status"""
        try:
            user = User.query.get(user_id)
            if not user:
                return {"error": "User not found"}
            
            preferences = json.loads(user.preferences) if user.preferences else {}
            
            return {
                "user_id": user_id,
                "consents": {
                    "email_notifications": preferences.get("email_notifications", False),
                    "data_processing": preferences.get("data_processing_consent", False),
                    "cookies": preferences.get("cookie_consent", False),
                    "marketing": preferences.get("marketing_consent", False)
                },
                "consent_date": preferences.get("consent_date"),
                "ip_address": preferences.get("consent_ip")
            }
            
        except Exception as e:
            logging.error(f"Error getting consent status: {e}")
            return {"error": str(e)}
    
    @staticmethod
    def update_consent(user_id: int, consent_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update user's consent preferences"""
        try:
            user = User.query.get(user_id)
            if not user:
                return {"error": "User not found"}
            
            preferences = json.loads(user.preferences) if user.preferences else {}
            
            # Update consent preferences
            preferences.update({
                "email_notifications": consent_data.get("email_notifications", False),
                "data_processing_consent": consent_data.get("data_processing", True),
                "cookie_consent": consent_data.get("cookies", True),
                "marketing_consent": consent_data.get("marketing", False),
                "consent_date": datetime.now().isoformat(),
                "consent_ip": consent_data.get("ip_address")
            })
            
            user.preferences = json.dumps(preferences)
            db.session.commit()
            
            return {
                "success": True,
                "message": "Consent preferences updated"
            }
            
        except Exception as e:
            logging.error(f"Error updating consent: {e}")
            db.session.rollback()
            return {"error": str(e)}