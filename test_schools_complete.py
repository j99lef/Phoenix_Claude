#!/usr/bin/env python3
"""Comprehensive test for schools/council functionality."""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import json
from travel_aigent import create_app
from travel_aigent.models import db, User, UserSchool

def test_schools_complete():
    """Test schools API functionality end-to-end."""
    app = create_app()
    
    with app.app_context():
        print("=" * 80)
        print("COMPREHENSIVE SCHOOLS API TEST")
        print("=" * 80)
        
        # 1. Check database setup
        print("\n1. DATABASE CHECK:")
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()
        print(f"   Tables in database: {tables}")
        
        if 'user_schools' not in tables:
            print("   ❌ user_schools table missing - creating...")
            db.create_all()
        else:
            print("   ✅ user_schools table exists")
        
        # 2. Check auth system
        print("\n2. AUTH SYSTEM CHECK:")
        from auth import auth
        
        # Create test client
        with app.test_client() as client:
            # Test without auth
            print("\n   Testing without authentication:")
            response = client.get('/api/schools')
            print(f"   GET /api/schools (no auth): {response.status_code}")
            if response.status_code == 401:
                print("   ✅ Auth protection working")
            else:
                print(f"   ❌ Unexpected response: {response.data}")
            
            # Login as admin
            print("\n   Testing with admin login:")
            with client.session_transaction() as sess:
                sess['username'] = 'admin'
                sess['authenticated'] = True
            
            # Test GET schools
            print("\n3. TESTING GET /api/schools:")
            response = client.get('/api/schools')
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.data.decode()}")
            
            if response.status_code == 200:
                schools = response.get_json()
                print(f"   ✅ Success! Found {len(schools)} schools")
            else:
                print(f"   ❌ Failed with status {response.status_code}")
                
            # Test POST school
            print("\n4. TESTING POST /api/schools:")
            test_school = {
                'school_key': 'westminster-council',
                'school_name': 'Westminster Council',
                'school_type': 'council',
                'region': 'London',
                'country': 'England',
                'is_primary': True,
                'child_name': 'Test Child'
            }
            
            response = client.post('/api/schools',
                                 data=json.dumps(test_school),
                                 content_type='application/json')
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.data.decode()}")
            
            if response.status_code == 201:
                created_school = response.get_json()
                print(f"   ✅ School created with ID: {created_school.get('id')}")
                school_id = created_school.get('id')
                
                # Test GET schools again
                print("\n5. VERIFYING SCHOOL WAS SAVED:")
                response = client.get('/api/schools')
                if response.status_code == 200:
                    schools = response.get_json()
                    print(f"   ✅ Now have {len(schools)} schools")
                    
                # Test DELETE
                if school_id:
                    print(f"\n6. TESTING DELETE /api/schools/{school_id}:")
                    response = client.delete(f'/api/schools/{school_id}')
                    print(f"   Status: {response.status_code}")
                    print(f"   Response: {response.data.decode()}")
                    
            elif response.status_code == 400:
                error = response.get_json()
                if 'already added' in error.get('error', ''):
                    print("   ℹ️  School already exists for this user")
                else:
                    print(f"   ❌ Bad request: {error}")
            else:
                print(f"   ❌ Failed to create school")
        
        # 7. Direct database check
        print("\n7. DIRECT DATABASE CHECK:")
        
        # Check if admin user exists
        admin_user = User.query.filter_by(username='admin').first()
        if admin_user:
            print(f"   ✅ Admin user exists (ID: {admin_user.id})")
            school_count = UserSchool.query.filter_by(user_id=admin_user.id).count()
            print(f"   Schools for admin: {school_count}")
        else:
            print("   ⚠️  Admin user not in database (using auth fallback)")
            
        # Check auth.get_current_user()
        print("\n8. TESTING auth.get_current_user():")
        
        # Simulate session
        from flask import Flask, session
        test_app = Flask(__name__)
        with test_app.test_request_context():
            session['username'] = 'admin'
            session['authenticated'] = True
            
            with app.app_context():
                user = auth.get_current_user()
                if user:
                    print(f"   ✅ get_current_user() returned: {user.username} (ID: {user.id})")
                else:
                    print("   ❌ get_current_user() returned None")
        
        print("\n" + "=" * 80)
        print("TEST COMPLETE")
        print("=" * 80)

if __name__ == "__main__":
    test_schools_complete()