"""School/Council management routes for TravelAiGent"""

from flask import Blueprint, request, jsonify, session
from auth import require_auth
from ..models import db, UserSchool, User

schools = Blueprint('schools', __name__)

@schools.route('/api/schools', methods=['GET'])
@require_auth
def get_user_schools():
    """Get all schools/councils for the current user"""
    try:
        username = session.get('username', 'admin')
        user = User.query.filter_by(username=username).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404
            
        user_schools = UserSchool.query.filter_by(user_id=user.id).all()
        return jsonify([school.to_dict() for school in user_schools])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@schools.route('/api/schools', methods=['POST'])
@require_auth
def add_user_school():
    """Add a new school/council for the current user"""
    try:
        username = session.get('username', 'admin')
        user = User.query.filter_by(username=username).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404
            
        data = request.get_json()
        
        # Validate required fields
        if not data.get('school_key') or not data.get('school_name'):
            return jsonify({'error': 'School key and name are required'}), 400
        
        # Check if school already exists for this user
        existing_school = UserSchool.query.filter_by(
            user_id=user.id,
            school_key=data['school_key']
        ).first()
        
        if existing_school:
            return jsonify({'error': 'This school is already added to your profile'}), 400
        
        # If this is being set as primary, unset any existing primary
        if data.get('is_primary', False):
            UserSchool.query.filter_by(
                user_id=user.id,
                is_primary=True
            ).update({'is_primary': False})
        
        # Create new school record
        school = UserSchool(
            user_id=user.id,
            school_key=data['school_key'],
            school_name=data['school_name'],
            school_type=data.get('school_type'),
            region=data.get('region'),
            country=data.get('country'),
            is_primary=data.get('is_primary', False),
            child_name=data.get('child_name')
        )
        
        db.session.add(school)
        db.session.commit()
        
        return jsonify(school.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@schools.route('/api/schools/<int:school_id>', methods=['DELETE'])
@require_auth
def delete_user_school(school_id):
    """Delete a school/council for the current user"""
    try:
        username = session.get('username', 'admin')
        user = User.query.filter_by(username=username).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404
            
        school = UserSchool.query.filter_by(
            id=school_id,
            user_id=user.id
        ).first()
        
        if not school:
            return jsonify({'error': 'School not found'}), 404
        
        db.session.delete(school)
        db.session.commit()
        
        return jsonify({'message': 'School removed successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@schools.route('/api/schools/<int:school_id>', methods=['PUT'])
@require_auth
def update_user_school(school_id):
    """Update a school/council for the current user"""
    try:
        username = session.get('username', 'admin')
        user = User.query.filter_by(username=username).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404
            
        school = UserSchool.query.filter_by(
            id=school_id,
            user_id=user.id
        ).first()
        
        if not school:
            return jsonify({'error': 'School not found'}), 404
        
        data = request.get_json()
        
        # If this is being set as primary, unset any existing primary
        if data.get('is_primary', False) and not school.is_primary:
            UserSchool.query.filter_by(
                user_id=user.id,
                is_primary=True
            ).update({'is_primary': False})
        
        # Update school fields
        school.child_name = data.get('child_name', school.child_name)
        school.is_primary = data.get('is_primary', school.is_primary)
        
        db.session.commit()
        
        return jsonify(school.to_dict()), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500