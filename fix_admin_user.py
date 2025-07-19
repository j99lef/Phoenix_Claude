#!/usr/bin/env python3
"""Fix admin user in database to ensure schools and deals work properly."""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from travel_aigent import create_app
from travel_aigent.models import db, User
from argon2 import PasswordHasher

def ensure_admin_user():
    """Ensure admin user exists in database with proper ID."""
    app = create_app()
    ph = PasswordHasher()
    
    with app.app_context():
        print("Checking admin user in database...")
        
        # Check if admin exists
        admin = User.query.filter_by(username='admin').first()
        
        if not admin:
            print("Admin user not found - creating...")
            
            # Get admin password from environment or use default
            admin_password = os.environ.get("ADMIN_PASSWORD", "changeme123!")
            
            # Create admin user
            admin = User(
                username='admin',
                email='admin@travelaigent.com',
                password_hash=ph.hash(admin_password),
                first_name='Admin',
                last_name='User'
            )
            
            db.session.add(admin)
            db.session.commit()
            
            print(f"✅ Created admin user with ID: {admin.id}")
        else:
            print(f"✅ Admin user exists with ID: {admin.id}")
            
        # Verify admin can be retrieved
        test_admin = User.query.filter_by(username='admin').first()
        if test_admin:
            print(f"✅ Admin user verified: {test_admin.username} (ID: {test_admin.id})")
        else:
            print("❌ Failed to retrieve admin user!")
            
        return admin.id if admin else None

if __name__ == "__main__":
    admin_id = ensure_admin_user()
    if admin_id:
        print(f"\nAdmin user ready with ID: {admin_id}")
        print("This will fix schools/council and deals functionality.")
    else:
        print("\n❌ Failed to create admin user!")