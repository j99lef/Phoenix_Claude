#!/usr/bin/env python3
"""Migrate database to add new columns."""

import os
import sys
from travel_aigent import create_app
from travel_aigent.models import db
from sqlalchemy import text

def migrate_database():
    """Add missing columns to existing tables."""
    app = create_app()
    
    with app.app_context():
        try:
            # Add new columns to travel_briefs table
            migrations = [
                "ALTER TABLE travel_briefs ADD COLUMN status VARCHAR(20) DEFAULT 'active'",
                "ALTER TABLE travel_briefs ADD COLUMN last_deal_check DATETIME",
                "ALTER TABLE travel_briefs ADD COLUMN deal_notifications BOOLEAN DEFAULT 1",
                "ALTER TABLE travel_briefs ADD COLUMN email_notifications BOOLEAN DEFAULT 1", 
                "ALTER TABLE travel_briefs ADD COLUMN sms_notifications BOOLEAN DEFAULT 0"
            ]
            
            print("🔄 Running migrations...")
            
            for migration in migrations:
                try:
                    db.session.execute(text(migration))
                    db.session.commit()
                    print(f"✅ Added column: {migration.split('COLUMN')[1].split()[0]}")
                except Exception as e:
                    db.session.rollback()
                    if "duplicate column name" in str(e).lower() or "already exists" in str(e).lower():
                        print(f"ℹ️  Column already exists: {migration.split('COLUMN')[1].split()[0]}")
                    else:
                        print(f"❌ Error adding column: {e}")
            
            print("\n✅ Migration completed!")
            
        except Exception as e:
            print(f"\n❌ Migration error: {e}")
            sys.exit(1)

if __name__ == '__main__':
    migrate_database()