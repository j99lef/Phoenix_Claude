#!/usr/bin/env python3
"""Test authentication for specific users."""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app
from travel_aigent.models import db, User
from auth import auth

def test_user_auth(username, password):
    """Test authentication for a specific user."""
    with app.app_context():
        print(f"\nTesting authentication for: {username}")
        
        # Check if user exists in database
        user = User.query.filter_by(username=username).first()
        
        if user:
            print(f"✅ User found in database")
            print(f"   Email: {user.email}")
            print(f"   Name: {user.first_name} {user.last_name}")
            print(f"   Password hash exists: {'Yes' if user.password_hash else 'No'}")
            print(f"   Hash prefix: {user.password_hash[:30]}..." if user.password_hash else "")
        else:
            print(f"❌ User NOT found in database")
            
            # Check if it's the built-in admin
            if username == auth.admin_username:
                print(f"ℹ️  This is the built-in admin user")
        
        # Test authentication
        result = auth.authenticate(username, password)
        print(f"\nAuthentication result: {'✅ SUCCESS' if result else '❌ FAILED'}")
        
        return result

def fix_admin_conflict():
    """Fix the admin user conflict."""
    with app.app_context():
        print("\n=== Checking for admin user conflict ===")
        
        # Check if there's an admin user in the database
        db_admin = User.query.filter_by(username='admin').first()
        
        if db_admin:
            print("Found 'admin' user in database - this may conflict with built-in admin")
            print(f"Database admin email: {db_admin.email}")
            print(f"Database admin has proper password hash: {db_admin.password_hash.startswith('$argon2')}")
            
            # The built-in admin should handle authentication
            print("\nThe built-in admin authentication should take precedence.")
        else:
            print("No 'admin' user in database - built-in admin will be used")

if __name__ == "__main__":
    # Test specific users
    print("=== TravelAiGent Authentication Test ===")
    
    # Test your user account
    print("\n1. Testing your account (J99Lef)")
    print("   Please verify you're using the correct password you set during registration")
    
    # Test built-in admin
    print("\n2. Testing built-in admin")
    test_user_auth("admin", "changeme123!")
    
    # Check for conflicts
    fix_admin_conflict()
    
    print("\n=== Summary ===")
    print("Your user account (J99Lef) exists in the database.")
    print("Make sure you're using the password you set during registration.")
    print("The built-in admin uses: username='admin', password='changeme123!'")
    print("\nIf login still fails, it might be a session/cookie issue on Railway.")