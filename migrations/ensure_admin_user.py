#!/usr/bin/env python3
"""Migration to ensure admin user exists in database for Railway deployment."""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from travel_aigent import create_app
from travel_aigent.models import db, User
from argon2 import PasswordHasher

def run_migration():
    """Ensure admin user exists in database."""
    app = create_app()
    ph = PasswordHasher()
    
    with app.app_context():
        print("Running admin user migration...")
        
        # Check if admin exists
        admin = User.query.filter_by(username='admin').first()
        
        if not admin:
            print("Creating admin user...")
            
            # Get admin credentials from environment
            admin_username = os.environ.get("ADMIN_USERNAME", "admin")
            admin_password = os.environ.get("ADMIN_PASSWORD", "changeme123!")
            
            # Create admin user
            admin = User(
                username=admin_username,
                email='admin@travelaigent.com',
                password_hash=ph.hash(admin_password),
                first_name='Admin',
                last_name='User'
            )
            
            db.session.add(admin)
            db.session.commit()
            
            print(f"✅ Created admin user: {admin_username} (ID: {admin.id})")
        else:
            print(f"✅ Admin user already exists: {admin.username} (ID: {admin.id})")
            
            # Update password if environment variable changed
            admin_password = os.environ.get("ADMIN_PASSWORD")
            if admin_password and not admin_password.startswith("$argon2"):
                print("Updating admin password from environment...")
                admin.password_hash = ph.hash(admin_password)
                db.session.commit()
                print("✅ Admin password updated")
                
        print("Migration complete!")

if __name__ == "__main__":
    run_migration()