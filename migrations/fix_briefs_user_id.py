#!/usr/bin/env python3
"""Fix travel briefs that don't have user_id set."""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app
from travel_aigent.models import db, TravelBrief, User
import logging

def fix_briefs_user_id():
    """Associate orphaned briefs with their users based on session data."""
    with app.app_context():
        logging.info("Checking for briefs without user_id...")
        
        # Find briefs without user_id
        orphaned_briefs = TravelBrief.query.filter_by(user_id=None).all()
        
        if not orphaned_briefs:
            print("✅ All briefs have user_id set correctly")
            return True
        
        print(f"Found {len(orphaned_briefs)} briefs without user_id")
        
        # For now, we'll need to manually associate these
        # In production, you might have logs or other data to help
        
        # List all users
        users = User.query.all()
        print("\nAvailable users:")
        for user in users:
            print(f"  {user.id}: {user.username} ({user.email})")
        
        # List orphaned briefs
        print(f"\nOrphaned briefs:")
        for brief in orphaned_briefs:
            print(f"  Brief ID {brief.id}: {brief.destination} ({brief.created_at})")
        
        # If you know which user created these briefs, you can update them:
        # For example, if user J99Lef (ID 2) created the briefs:
        j99lef_user = User.query.filter_by(username='J99Lef').first()
        if j99lef_user and orphaned_briefs:
            print(f"\nAssociating {len(orphaned_briefs)} briefs with user {j99lef_user.username}...")
            for brief in orphaned_briefs:
                brief.user_id = j99lef_user.id
            db.session.commit()
            print("✅ Briefs updated successfully")
            return True
        
        print("\n⚠️  Manual intervention needed to associate briefs with users")
        return False

if __name__ == "__main__":
    if fix_briefs_user_id():
        print("\n✅ Migration completed successfully")
    else:
        print("\n⚠️  Migration needs manual intervention")
        sys.exit(1)