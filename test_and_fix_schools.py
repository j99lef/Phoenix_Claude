#!/usr/bin/env python3
"""Test and fix schools functionality."""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import json
import time
from travel_aigent import create_app
from travel_aigent.models import db, User, UserSchool
from flask import session
from auth import auth as auth_system

def test_and_fix():
    """Test schools and fix any issues found."""
    app = create_app()
    
    with app.app_context():
        print("=" * 80)
        print("TESTING AND FIXING SCHOOLS FUNCTIONALITY")
        print("=" * 80)
        
        # 1. Ensure admin exists
        print("\n1. Checking admin user:")
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            print("   ❌ Admin not found - run: python migrations/ensure_admin_user.py")
            return
        print(f"   ✅ Admin exists (ID: {admin.id})")
        
        # 2. Test the actual route with proper authentication
        print("\n2. Testing schools route with proper session:")
        
        with app.test_request_context('/api/schools'):
            # Properly set up session as if user logged in
            session['username'] = 'admin'
            session['authenticated'] = True
            session['login_time'] = time.time()
            session.permanent = True
            
            # Test get_current_user
            user = auth_system.get_current_user()
            if user:
                print(f"   ✅ get_current_user() works: {user.username} (ID: {user.id})")
            else:
                print("   ❌ get_current_user() failed!")
                print(f"   Session data: {dict(session)}")
                print(f"   Is authenticated: {auth_system.is_authenticated()}")
                
        # 3. Test adding a school directly to database
        print("\n3. Adding test school directly to database:")
        
        # Check if test school already exists
        existing = UserSchool.query.filter_by(
            user_id=admin.id,
            school_key='test-school'
        ).first()
        
        if existing:
            print("   Removing existing test school...")
            db.session.delete(existing)
            db.session.commit()
        
        # Add test school
        test_school = UserSchool(
            user_id=admin.id,
            school_key='test-school',
            school_name='Test School',
            school_type='council',
            region='London',
            country='England',
            is_primary=True
        )
        
        db.session.add(test_school)
        db.session.commit()
        print(f"   ✅ Added test school (ID: {test_school.id})")
        
        # 4. Test retrieval
        print("\n4. Testing school retrieval:")
        schools = UserSchool.query.filter_by(user_id=admin.id).all()
        print(f"   Found {len(schools)} schools for admin:")
        for school in schools:
            print(f"   - {school.school_name} ({school.school_type}) ID: {school.id}")
            
        # 5. Test the API endpoint manually
        print("\n5. Testing API endpoint manually:")
        
        # Import the view function
        from travel_aigent.routes.schools import get_user_schools
        
        with app.test_request_context('/api/schools'):
            # Set up proper session
            session['username'] = 'admin'
            session['authenticated'] = True
            session['login_time'] = time.time()
            
            # Manually check what happens in the route
            print("   Checking route logic:")
            
            # This is what happens in the route
            from auth import auth
            current_user = auth.get_current_user()
            
            if current_user:
                print(f"   ✅ Route would get user: {current_user.username} (ID: {current_user.id})")
                
                # What the route would return
                user_schools = UserSchool.query.filter_by(user_id=current_user.id).all()
                schools_data = [school.to_dict() for school in user_schools]
                print(f"   ✅ Route would return {len(schools_data)} schools")
                print(f"   Data: {json.dumps(schools_data, indent=2)}")
            else:
                print("   ❌ Route would fail - no user!")
                
        print("\n" + "=" * 80)
        print("DIAGNOSTIC SUMMARY:")
        print("=" * 80)
        print(f"✅ Admin user exists in database: ID {admin.id}")
        print(f"✅ Schools table exists and works")
        print(f"✅ Can add/retrieve schools directly")
        print(f"{'✅' if user else '❌'} auth.get_current_user() works in request context")
        print("\nThe issue is likely that the session is not being set properly")
        print("when logging in through the web interface.")
        print("=" * 80)

if __name__ == "__main__":
    test_and_fix()