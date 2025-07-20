#!/usr/bin/env python3
"""Test that admin user is automatically created."""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from travel_aigent import create_app
from travel_aigent.models import db, User

def test_auto_admin_creation():
    """Test automatic admin user creation."""
    # Remove existing database to test fresh
    if os.path.exists('travel_aigent.db'):
        os.remove('travel_aigent.db')
        print("Removed existing database")
    
    print("Creating fresh app...")
    app = create_app()
    
    with app.app_context():
        print("\nChecking admin user...")
        admin = User.query.filter_by(username='admin').first()
        
        if admin:
            print(f"✅ SUCCESS: Admin user automatically created!")
            print(f"   Username: {admin.username}")
            print(f"   ID: {admin.id}")
            print(f"   Email: {admin.email}")
            
            # Test authentication
            from auth import auth
            if auth.authenticate('admin', 'changeme123!'):
                print("✅ Authentication works!")
            else:
                print("❌ Authentication failed!")
                
        else:
            print("❌ FAILED: Admin user not created automatically")
            
        # Check all users
        user_count = User.query.count()
        print(f"\nTotal users in database: {user_count}")

if __name__ == "__main__":
    test_auto_admin_creation()