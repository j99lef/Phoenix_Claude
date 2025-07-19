#!/usr/bin/env python3
"""Simple test for schools functionality."""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from travel_aigent import create_app
from travel_aigent.models import db, User, UserSchool
from flask import session
import json

def test_schools_functionality():
    """Test schools functionality directly."""
    app = create_app()
    
    with app.app_context():
        print("=" * 80)
        print("TESTING SCHOOLS FUNCTIONALITY")
        print("=" * 80)
        
        # 1. Check admin user
        print("\n1. Checking admin user:")
        admin = User.query.filter_by(username='admin').first()
        if admin:
            print(f"   ✅ Admin user exists (ID: {admin.id})")
        else:
            print("   ❌ Admin user not found!")
            return
            
        # 2. Test auth.get_current_user()
        print("\n2. Testing auth.get_current_user():")
        from auth import auth
        
        # Create a test request context with session
        with app.test_request_context():
            # Simulate logged in admin
            session['username'] = 'admin'
            session['authenticated'] = True
            
            user = auth.get_current_user()
            if user:
                print(f"   ✅ get_current_user() works: {user.username} (ID: {user.id})")
            else:
                print("   ❌ get_current_user() returned None")
                
        # 3. Test schools API directly
        print("\n3. Testing schools API endpoints directly:")
        
        # Import the routes
        from travel_aigent.routes.schools import get_user_schools, add_user_school
        
        with app.test_request_context('/api/schools', method='GET'):
            session['username'] = 'admin'
            session['authenticated'] = True
            
            try:
                response = get_user_schools()
                if isinstance(response, tuple):
                    data, status = response
                else:
                    data = response
                    status = 200
                    
                print(f"   GET /api/schools: Status {status}")
                
                if status == 200:
                    schools = json.loads(data.data) if hasattr(data, 'data') else data
                    print(f"   ✅ Found {len(schools)} schools")
                else:
                    print(f"   ❌ Error: {data}")
                    
            except Exception as e:
                print(f"   ❌ Exception: {e}")
                
        # 4. Test adding a school
        print("\n4. Testing add school directly:")
        
        test_school = {
            'school_key': 'test-council',
            'school_name': 'Test Council',
            'school_type': 'council',
            'region': 'London',
            'country': 'England',
            'is_primary': True
        }
        
        with app.test_request_context('/api/schools', method='POST',
                                    data=json.dumps(test_school),
                                    content_type='application/json'):
            session['username'] = 'admin'
            session['authenticated'] = True
            
            try:
                response = add_user_school()
                if isinstance(response, tuple):
                    data, status = response
                else:
                    data = response
                    status = 200
                    
                print(f"   POST /api/schools: Status {status}")
                
                if status == 201:
                    print("   ✅ School added successfully")
                elif status == 400:
                    error_data = json.loads(data.data) if hasattr(data, 'data') else data
                    print(f"   ⚠️  {error_data.get('error', 'Unknown error')}")
                else:
                    print(f"   ❌ Error: {data}")
                    
            except Exception as e:
                print(f"   ❌ Exception: {e}")
                import traceback
                traceback.print_exc()
                
        # 5. Check database directly
        print("\n5. Checking database directly:")
        schools_count = UserSchool.query.filter_by(user_id=admin.id).count()
        print(f"   Schools for admin user: {schools_count}")
        
        if schools_count > 0:
            schools = UserSchool.query.filter_by(user_id=admin.id).all()
            for school in schools:
                print(f"   - {school.school_name} ({school.school_type})")
                
        print("\n" + "=" * 80)
        print("TEST COMPLETE")
        print("=" * 80)

if __name__ == "__main__":
    # Ensure admin exists first
    import subprocess
    subprocess.run([sys.executable, "fix_admin_user.py"])
    
    test_schools_functionality()