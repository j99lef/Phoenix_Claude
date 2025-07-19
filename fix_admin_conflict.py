#!/usr/bin/env python3
"""Fix admin user conflict by removing database admin user."""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app
from travel_aigent.models import db, User

def fix_admin_conflict():
    """Remove the conflicting admin user from database."""
    with app.app_context():
        print("\n=== Fixing Admin User Conflict ===\n")
        
        # Find the admin user in database
        db_admin = User.query.filter_by(username='admin').first()
        
        if db_admin:
            print(f"Found conflicting admin user:")
            print(f"  ID: {db_admin.id}")
            print(f"  Username: {db_admin.username}")
            print(f"  Email: {db_admin.email}")
            print(f"  Password Hash: {db_admin.password_hash[:30]}...")
            
            # Check if it has the temporary hash
            if db_admin.password_hash == 'temp_hash':
                print("\n⚠️  This admin user has a temporary hash and is causing conflicts.")
                print("Removing this user to allow built-in admin authentication to work...")
                
                # Delete the user
                db.session.delete(db_admin)
                db.session.commit()
                
                print("✅ Conflicting admin user removed successfully!")
                print("\nYou can now login with:")
                print("  Username: admin")
                print("  Password: changeme123!")
            else:
                print("\n⚠️  This admin user has a real password hash.")
                print("It might be a legitimate user. Not removing automatically.")
        else:
            print("✅ No conflicting admin user found in database.")
            print("Built-in admin authentication should work properly.")
        
        # List remaining users
        print("\n=== Remaining Users ===")
        users = User.query.all()
        for user in users:
            print(f"- {user.username} ({user.email})")
        
        print(f"\nTotal users: {len(users)}")

if __name__ == "__main__":
    fix_admin_conflict()