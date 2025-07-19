#!/usr/bin/env python3
"""Fix admin user conflict in production database."""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app
from travel_aigent.models import db, User
import logging

def fix_admin_user():
    """Remove conflicting admin user with temp_hash."""
    with app.app_context():
        logging.info("Starting admin user fix migration...")
        
        # Find admin user with temp_hash
        db_admin = User.query.filter_by(username='admin').first()
        
        if db_admin and db_admin.password_hash == 'temp_hash':
            logging.info(f"Found conflicting admin user with ID {db_admin.id}")
            
            # Delete the conflicting user
            db.session.delete(db_admin)
            db.session.commit()
            
            logging.info("Conflicting admin user removed successfully")
            print("✅ Admin user conflict fixed")
            return True
        elif db_admin:
            logging.info("Admin user exists but has a proper password hash")
            print("ℹ️  Admin user has proper password hash, no action needed")
            return True
        else:
            logging.info("No admin user found in database")
            print("✅ No admin conflict found")
            return True

if __name__ == "__main__":
    if fix_admin_user():
        print("\n✅ Migration completed successfully")
        print("\nYou can now login with:")
        print("  - Your account: J99Lef")
        print("  - Admin account: admin / changeme123!")
    else:
        print("\n❌ Migration failed")
        sys.exit(1)