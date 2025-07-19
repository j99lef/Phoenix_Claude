#!/usr/bin/env python3
"""Add password_reset_tokens table for secure password recovery."""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app
from travel_aigent.models import db, PasswordResetToken

def run_migration():
    """Create password_reset_tokens table."""
    with app.app_context():
        # Create the table
        db.create_all()
        
        # Verify table exists
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        
        if 'password_reset_tokens' in tables:
            print("✅ Successfully created password_reset_tokens table")
            
            # Get column info
            columns = inspector.get_columns('password_reset_tokens')
            print("\nTable structure:")
            for col in columns:
                print(f"  - {col['name']}: {col['type']}")
        else:
            print("❌ Failed to create password_reset_tokens table")
            return False
        
        return True

if __name__ == "__main__":
    if run_migration():
        print("\n✅ Migration completed successfully")
    else:
        print("\n❌ Migration failed")
        sys.exit(1)