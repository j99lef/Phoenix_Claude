"""Routes for managing people profiles"""
from flask import Blueprint, request, jsonify, session
from sqlalchemy.exc import SQLAlchemyError
import logging

from ..models import db, Person, User
from auth import require_auth

bp = Blueprint("people", __name__)


@bp.route("/api/people", methods=["GET"])
@require_auth
def get_people():
    """Get all people profiles for the current user"""
    try:
        username = session.get('username', 'user')
        user = User.query.filter_by(username=username).first()
        
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        people = Person.query.filter_by(user_id=user.id).all()
        return jsonify([person.to_dict() for person in people])
        
    except Exception as e:
        logging.error(f"Error fetching people: {e}")
        return jsonify({"error": "Failed to fetch people"}), 500


@bp.route("/api/people", methods=["POST"])
@require_auth
def create_person():
    """Create a new person profile"""
    try:
        username = session.get('username', 'user')
        user = User.query.filter_by(username=username).first()
        
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        data = request.get_json()
        
        # Validate required fields
        if not data.get('first_name'):
            return jsonify({"error": "First name is required"}), 400
        
        # Parse date fields
        from datetime import datetime
        date_of_birth = None
        if data.get('date_of_birth'):
            try:
                date_of_birth = datetime.fromisoformat(data['date_of_birth']).date()
            except:
                pass
        
        passport_expiry = None
        if data.get('passport_expiry'):
            try:
                passport_expiry = datetime.fromisoformat(data['passport_expiry']).date()
            except:
                pass
        
        # Create new person
        person = Person(
            user_id=user.id,
            first_name=data['first_name'],
            last_name=data.get('last_name'),
            nickname=data.get('nickname'),
            date_of_birth=date_of_birth,
            person_type=data.get('person_type', 'adult'),
            passport_number=data.get('passport_number'),
            passport_expiry=passport_expiry,
            dietary_restrictions=data.get('dietary_restrictions'),
            medical_notes=data.get('medical_notes')
        )
        
        db.session.add(person)
        db.session.commit()
        
        return jsonify(person.to_dict()), 201
        
    except Exception as e:
        logging.error(f"Error creating person: {e}")
        db.session.rollback()
        return jsonify({"error": "Failed to create person"}), 500


@bp.route("/api/people/<int:person_id>", methods=["PUT"])
@require_auth
def update_person(person_id):
    """Update a person profile"""
    try:
        username = session.get('username', 'user')
        user = User.query.filter_by(username=username).first()
        
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        person = Person.query.filter_by(id=person_id, user_id=user.id).first()
        if not person:
            return jsonify({"error": "Person not found"}), 404
        
        data = request.get_json()
        
        # Update fields
        if 'first_name' in data:
            person.first_name = data['first_name']
        if 'last_name' in data:
            person.last_name = data['last_name']
        if 'nickname' in data:
            person.nickname = data['nickname']
        if 'person_type' in data:
            person.person_type = data['person_type']
        if 'passport_number' in data:
            person.passport_number = data['passport_number']
        if 'dietary_restrictions' in data:
            person.dietary_restrictions = data['dietary_restrictions']
        if 'medical_notes' in data:
            person.medical_notes = data['medical_notes']
        
        # Parse date fields
        from datetime import datetime
        if 'date_of_birth' in data:
            if data['date_of_birth']:
                try:
                    person.date_of_birth = datetime.fromisoformat(data['date_of_birth']).date()
                except:
                    pass
            else:
                person.date_of_birth = None
        
        if 'passport_expiry' in data:
            if data['passport_expiry']:
                try:
                    person.passport_expiry = datetime.fromisoformat(data['passport_expiry']).date()
                except:
                    pass
            else:
                person.passport_expiry = None
        
        db.session.commit()
        return jsonify(person.to_dict())
        
    except Exception as e:
        logging.error(f"Error updating person: {e}")
        db.session.rollback()
        return jsonify({"error": "Failed to update person"}), 500


@bp.route("/api/people/<int:person_id>", methods=["DELETE"])
@require_auth
def delete_person(person_id):
    """Delete a person profile"""
    try:
        username = session.get('username', 'user')
        user = User.query.filter_by(username=username).first()
        
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        person = Person.query.filter_by(id=person_id, user_id=user.id).first()
        if not person:
            return jsonify({"error": "Person not found"}), 404
        
        # Check if person is in any groups
        from ..models import GroupMember
        memberships = GroupMember.query.filter_by(person_id=person_id).count()
        if memberships > 0:
            return jsonify({"error": f"Cannot delete person who is in {memberships} group(s)"}), 400
        
        db.session.delete(person)
        db.session.commit()
        
        return jsonify({"message": "Person deleted successfully"}), 200
        
    except Exception as e:
        logging.error(f"Error deleting person: {e}")
        db.session.rollback()
        return jsonify({"error": "Failed to delete person"}), 500