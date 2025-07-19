"""Routes for managing travel groups"""
import json
from flask import Blueprint, jsonify, request, session
from ..models import db, TravelGroup, User
from auth import require_auth

groups_bp = Blueprint('groups', __name__)


@groups_bp.route('/api/groups', methods=['GET'])
@require_auth
def get_groups():
    """Get all travel groups for the current user"""
    username = session.get('username', 'admin')
    
    try:
        # Get user from database
        user = User.query.filter_by(username=username).first()
        if not user:
            # Create default user if doesn't exist
            user = User(
                username=username,
                email=f"{username}@travelaigent.com",
                password_hash="temp_hash",
                first_name="",
                last_name="",
                adults_count=2,
                travel_style="luxury"
            )
            db.session.add(user)
            db.session.commit()
        
        groups = TravelGroup.query.filter_by(user_id=user.id).all()
        return jsonify([group.to_dict() for group in groups])
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@groups_bp.route('/api/groups', methods=['POST'])
@require_auth
def create_group():
    """Create a new travel group"""
    username = session.get('username', 'admin')
    data = request.get_json()
    
    try:
        # Get user from database
        user = User.query.filter_by(username=username).first()
        if not user:
            # Create default user if doesn't exist
            user = User(
                username=username,
                email=f"{username}@travelaigent.com",
                password_hash="temp_hash",
                first_name="",
                last_name="",
                adults_count=2,
                travel_style="luxury"
            )
            db.session.add(user)
            db.session.commit()
            # Refresh user to get the ID
            user = User.query.filter_by(username=username).first()
        
        # Ensure user exists and has valid ID
        if not user or not user.id:
            return jsonify({'error': 'Failed to create or find user'}), 500
        
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


@groups_bp.route('/api/groups/<int:group_id>', methods=['PUT'])
@require_auth
def update_group(group_id):
    """Update an existing travel group"""
    username = session.get('username', 'admin')
    data = request.get_json()
    
    try:
        # Get user from database
        user = User.query.filter_by(username=username).first()
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
    username = session.get('username', 'admin')
    
    try:
        # Get user from database
        user = User.query.filter_by(username=username).first()
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
    username = session.get('username', 'admin')
    
    try:
        # Get user from database
        user = User.query.filter_by(username=username).first()
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