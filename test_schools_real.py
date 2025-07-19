#!/usr/bin/env python3
"""Real test for schools API using proper Flask context."""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import json
import requests
from travel_aigent import create_app
from travel_aigent.models import db, User, UserSchool
import threading
import time

def run_test_server(app):
    """Run Flask app in a thread for testing."""
    app.run(host='127.0.0.1', port=5555, debug=False, use_reloader=False)

def test_schools_api():
    """Test schools API with real HTTP requests."""
    app = create_app()
    
    # Start server in background
    server_thread = threading.Thread(target=run_test_server, args=(app,), daemon=True)
    server_thread.start()
    time.sleep(2)  # Wait for server to start
    
    base_url = "http://127.0.0.1:5555"
    
    print("=" * 80)
    print("TESTING SCHOOLS API WITH REAL REQUESTS")
    print("=" * 80)
    
    # Create a session to maintain cookies
    session = requests.Session()
    
    # Test 1: Try to access schools without login
    print("\n1. Testing /api/schools without authentication:")
    response = session.get(f"{base_url}/api/schools")
    print(f"   Status: {response.status_code}")
    if response.status_code == 401:
        print("   ✅ Auth required as expected")
    else:
        print(f"   Response: {response.text}")
    
    # Test 2: Login as admin
    print("\n2. Logging in as admin:")
    login_data = {
        'username': 'admin',
        'password': 'changeme123!'
    }
    response = session.post(f"{base_url}/login", data=login_data)
    print(f"   Status: {response.status_code}")
    if response.status_code == 302:  # Redirect after successful login
        print("   ✅ Login successful")
    else:
        print(f"   ❌ Login failed: {response.text}")
        return
    
    # Test 3: Get schools after login
    print("\n3. Testing GET /api/schools after login:")
    response = session.get(f"{base_url}/api/schools")
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        schools = response.json()
        print(f"   ✅ Success! Found {len(schools)} schools")
        print(f"   Schools: {schools}")
    else:
        print(f"   ❌ Failed: {response.text}")
    
    # Test 4: Add a school
    print("\n4. Testing POST /api/schools:")
    test_school = {
        'school_key': 'camden-council',
        'school_name': 'Camden Council',
        'school_type': 'council',
        'region': 'London',
        'country': 'England',
        'is_primary': True,
        'child_name': 'Test Child'
    }
    
    response = session.post(f"{base_url}/api/schools",
                          json=test_school,
                          headers={'Content-Type': 'application/json'})
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 201:
        created_school = response.json()
        print(f"   ✅ School created successfully!")
        print(f"   School: {created_school}")
        school_id = created_school.get('id')
        
        # Test 5: Get schools again to verify
        print("\n5. Verifying school was saved:")
        response = session.get(f"{base_url}/api/schools")
        if response.status_code == 200:
            schools = response.json()
            print(f"   ✅ Now have {len(schools)} schools")
            
        # Test 6: Delete the school
        if school_id:
            print(f"\n6. Testing DELETE /api/schools/{school_id}:")
            response = session.delete(f"{base_url}/api/schools/{school_id}")
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                print("   ✅ School deleted successfully")
            else:
                print(f"   Response: {response.text}")
                
    elif response.status_code == 400:
        error = response.json()
        print(f"   ⚠️  {error.get('error', 'Unknown error')}")
    else:
        print(f"   ❌ Failed: {response.text}")
    
    print("\n" + "=" * 80)
    print("TEST COMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    # First ensure admin user exists
    print("Ensuring admin user exists...")
    import subprocess
    subprocess.run([sys.executable, "fix_admin_user.py"])
    
    print("\nStarting API test...")
    test_schools_api()