#!/usr/bin/env python3
"""Test script to diagnose schools API issues."""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from travel_aigent import create_app
from travel_aigent.models import db, User, UserSchool

def test_schools_api():
    """Test schools API functionality."""
    app = create_app()
    
    with app.app_context():
        print("Testing Schools API...")
        print("=" * 60)
        
        # Check if UserSchool table exists
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()
        if 'user_schools' in tables:
            print("✅ user_schools table exists")
        else:
            print("❌ user_schools table missing!")
            print("Creating table...")
            db.create_all()
            print("✅ Table created")
        
        # Check registered routes
        print("\nRegistered routes containing 'school':")
        for rule in app.url_map.iter_rules():
            if 'school' in rule.rule:
                methods = ','.join(rule.methods - {'HEAD', 'OPTIONS'})
                print(f"  {rule.rule} [{methods}]")
        
        # Test with client
        with app.test_client() as client:
            print("\nTesting API endpoints:")
            
            # Test GET /api/schools without auth
            response = client.get('/api/schools')
            print(f"\nGET /api/schools (no auth): {response.status_code}")
            if response.status_code == 401:
                print("✅ Auth required as expected")
            
            # Test with session
            with client.session_transaction() as sess:
                sess['username'] = 'admin'
                sess['authenticated'] = True
            
            response = client.get('/api/schools')
            print(f"\nGET /api/schools (with auth): {response.status_code}")
            if response.status_code == 200:
                print("✅ Schools API working!")
                print(f"Response: {response.get_json()}")
            elif response.status_code == 404:
                print("❌ Route not found")
            else:
                print(f"❌ Unexpected status: {response.text}")
        
        # Check if any schools exist in database
        school_count = UserSchool.query.count()
        print(f"\nTotal schools in database: {school_count}")
        
        # Check users
        user_count = User.query.count()
        print(f"Total users in database: {user_count}")
        
        if user_count > 0:
            print("\nSample users:")
            for user in User.query.limit(3).all():
                schools = UserSchool.query.filter_by(user_id=user.id).count()
                print(f"  - {user.username}: {schools} schools")

if __name__ == "__main__":
    test_schools_api()