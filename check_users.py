#!/usr/bin/env python3
"""Check user database and authentication issues."""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app
from travel_aigent.models import db, User
from auth import auth
from argon2 import PasswordHasher

def check_users():
    """Check all users in the database."""
    with app.app_context():
        print("\n=== User Database Check ===\n")
        
        # Check if tables exist
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        print(f"Available tables: {tables}\n")
        
        if 'users' not in tables:
            print("❌ Users table does not exist!")
            return
        
        # Get all users
        users = User.query.all()
        print(f"Total users in database: {len(users)}\n")
        
        # Display user details
        for user in users:
            print(f"User ID: {user.id}")
            print(f"  Username: {user.username}")
            print(f"  Email: {user.email}")
            print(f"  First Name: {user.first_name}")
            print(f"  Last Name: {user.last_name}")
            print(f"  Password Hash: {user.password_hash[:50]}..." if user.password_hash else "No password hash")
            print(f"  Created: {user.created_at}")
            print(f"  Last Login: {user.last_login}")
            print()
        
        # Check admin user
        print("\n=== Admin User Check ===")
        print(f"Admin username from env: {auth.admin_username}")
        print(f"Admin has password hash: {'Yes' if auth.admin_password_hash else 'No'}")
        
        # Test authentication
        print("\n=== Authentication Test ===")
        test_username = input("Enter username to test (or press Enter to skip): ").strip()
        if test_username:
            test_password = input("Enter password: ").strip()
            
            result = auth.authenticate(test_username, test_password)
            print(f"\nAuthentication result: {'✅ SUCCESS' if result else '❌ FAILED'}")
            
            if not result:
                # Check if user exists
                user = User.query.filter_by(username=test_username).first()
                if not user and test_username != auth.admin_username:
                    print("  Reason: User not found in database")
                else:
                    print("  Reason: Invalid password")

def test_password_hashing():
    """Test password hashing functionality."""
    print("\n=== Password Hashing Test ===")
    ph = PasswordHasher()
    
    test_password = "TestPassword123!"
    hash1 = ph.hash(test_password)
    print(f"Test password: {test_password}")
    print(f"Generated hash: {hash1[:50]}...")
    
    try:
        ph.verify(hash1, test_password)
        print("✅ Password verification successful")
    except Exception as e:
        print(f"❌ Password verification failed: {e}")

if __name__ == "__main__":
    check_users()
    test_password_hashing()