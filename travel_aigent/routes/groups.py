"""Routes for managing travel groups"""
import json
from flask import Blueprint, jsonify, request, session
from ..models import db, TravelGroup, User, UserSchoolCalendar, SchoolTermDates
from auth import require_auth, auth

groups_bp = Blueprint('groups', __name__)


@groups_bp.route('/api/groups', methods=['GET'])
@require_auth
def get_groups():
    """Get all travel groups for the current user"""
    try:
        # Get current user using auth system
        user = auth.get_current_user()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        groups = TravelGroup.query.filter_by(user_id=user.id).all()
        return jsonify([group.to_dict() for group in groups])
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@groups_bp.route('/api/groups', methods=['POST'])
@require_auth
def create_group():
    """Create a new travel group"""
    data = request.get_json()
    
    try:
        # Get current user using auth system
        user = auth.get_current_user()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Validate required fields
        if not data.get('group_name'):
            return jsonify({'error': 'Group name is required'}), 400
        
        if not data.get('members') or not isinstance(data['members'], list):
            return jsonify({'error': 'Members list is required'}), 400
        
        # Create new group
        group = TravelGroup(
            user_id=user.id,
            group_name=data['group_name'],
            group_type=data.get('group_type', 'custom'),
            members=json.dumps(data['members'])
        )
        
        db.session.add(group)
        db.session.commit()
        
        return jsonify(group.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@groups_bp.route('/api/groups/<int:group_id>', methods=['GET'])
@require_auth
def get_group(group_id):
    """Get a single travel group"""
    try:
        # Get current user using auth system
        user = auth.get_current_user()
        if not user:
            return jsonify({'error': 'User not found'}), 404
            
        group = TravelGroup.query.filter_by(id=group_id, user_id=user.id).first()
        if not group:
            return jsonify({'error': 'Group not found'}), 404
        
        return jsonify(group.to_dict())
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@groups_bp.route('/api/groups/<int:group_id>/calendar', methods=['GET'])
@require_auth
def get_group_calendar(group_id):
    """Get the school calendar for a travel group"""
    try:
        # Get current user using auth system
        user = auth.get_current_user()
        if not user:
            return jsonify({'error': 'User not found'}), 404
            
        group = TravelGroup.query.filter_by(id=group_id, user_id=user.id).first()
        if not group:
            return jsonify({'error': 'Group not found'}), 404
        
        # Get user's school calendar
        calendar = UserSchoolCalendar.query.filter_by(user_id=user.id).first()
        
        if not calendar:
            return jsonify({'error': 'No school calendar configured'}), 404
        
        # For now, return mock calendar data
        # In production, this would fetch from the actual calendar data
        from datetime import datetime, timedelta
        today = datetime.now()
        
        holidays = []
        
        # Add upcoming holidays based on country
        if calendar.country.lower() == 'england':
            holidays = [
                {
                    'name': 'February Half Term',
                    'start_date': (today + timedelta(days=30)).strftime('%Y-%m-%d'),
                    'end_date': (today + timedelta(days=37)).strftime('%Y-%m-%d')
                },
                {
                    'name': 'Easter Holidays',
                    'start_date': (today + timedelta(days=60)).strftime('%Y-%m-%d'),
                    'end_date': (today + timedelta(days=74)).strftime('%Y-%m-%d')
                },
                {
                    'name': 'May Half Term',
                    'start_date': (today + timedelta(days=100)).strftime('%Y-%m-%d'),
                    'end_date': (today + timedelta(days=107)).strftime('%Y-%m-%d')
                },
                {
                    'name': 'Summer Holidays',
                    'start_date': (today + timedelta(days=150)).strftime('%Y-%m-%d'),
                    'end_date': (today + timedelta(days=192)).strftime('%Y-%m-%d')
                }
            ]
        else:
            # Default holidays for other countries
            holidays = [
                {
                    'name': 'Spring Break',
                    'start_date': (today + timedelta(days=45)).strftime('%Y-%m-%d'),
                    'end_date': (today + timedelta(days=52)).strftime('%Y-%m-%d')
                },
                {
                    'name': 'Summer Vacation',
                    'start_date': (today + timedelta(days=120)).strftime('%Y-%m-%d'),
                    'end_date': (today + timedelta(days=183)).strftime('%Y-%m-%d')
                }
            ]
        
        return jsonify({
            'country': calendar.country,
            'holidays': holidays,
            'academic_year': f"{today.year}/{today.year + 1}"
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@groups_bp.route('/api/groups/<int:group_id>', methods=['PUT'])
@require_auth
def update_group(group_id):
    """Update an existing travel group"""
    data = request.get_json()
    
    try:
        # Get current user using auth system
        user = auth.get_current_user()
        if not user:
            return jsonify({'error': 'User not found'}), 404
            
        group = TravelGroup.query.filter_by(id=group_id, user_id=user.id).first()
        if not group:
            return jsonify({'error': 'Group not found'}), 404
        
        # Update fields
        if 'group_name' in data:
            group.group_name = data['group_name']
        if 'group_type' in data:
            group.group_type = data['group_type']
        if 'members' in data:
            group.members = json.dumps(data['members'])
        
        db.session.commit()
        return jsonify(group.to_dict())
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@groups_bp.route('/api/groups/<int:group_id>', methods=['DELETE'])
@require_auth
def delete_group(group_id):
    """Delete a travel group"""
    try:
        # Get current user using auth system
        user = auth.get_current_user()
        if not user:
            return jsonify({'error': 'User not found'}), 404
            
        group = TravelGroup.query.filter_by(id=group_id, user_id=user.id).first()
        if not group:
            return jsonify({'error': 'Group not found'}), 404
        
        db.session.delete(group)
        db.session.commit()
        
        return jsonify({'message': 'Group deleted successfully'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@groups_bp.route('/api/groups/<int:group_id>/set-primary', methods=['POST'])
@require_auth
def set_primary_group(group_id):
    """Set a group as the primary group"""
    try:
        # Get current user using auth system
        user = auth.get_current_user()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Find the group
        group = TravelGroup.query.filter_by(id=group_id, user_id=user.id).first()
        if not group:
            return jsonify({'error': 'Group not found'}), 404
        
        # Clear all other primary flags for this user
        TravelGroup.query.filter_by(user_id=user.id).update({'is_primary': False})
        
        # Set this group as primary
        group.is_primary = True
        db.session.commit()
        
        return jsonify({'message': 'Primary group updated'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500