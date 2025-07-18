#!/usr/bin/env python3
"""Railway database migration script."""

import os
import sys
from travel_aigent import create_app
from travel_aigent.models import db
from sqlalchemy import text, inspect

def run_migration():
    """Run database migrations for Railway deployment."""
    app = create_app()
    
    with app.app_context():
        print("🚂 Railway Database Migration")
        print("=" * 50)
        
        # First ensure all tables exist
        db.create_all()
        print("✅ Ensured all tables exist")
        
        # Check current schema
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        print(f"\n📊 Found tables: {', '.join(tables)}")
        
        # Check and add missing columns to travel_briefs
        if 'travel_briefs' in tables:
            columns = [col['name'] for col in inspector.get_columns('travel_briefs')]
            print(f"\n📋 Current columns in travel_briefs: {len(columns)}")
            
            # Define required columns and their SQL
            required_columns = {
                'status': "ALTER TABLE travel_briefs ADD COLUMN status VARCHAR(20) DEFAULT 'active'",
                'last_deal_check': "ALTER TABLE travel_briefs ADD COLUMN last_deal_check TIMESTAMP",
                'deal_notifications': "ALTER TABLE travel_briefs ADD COLUMN deal_notifications BOOLEAN DEFAULT TRUE",
                'email_notifications': "ALTER TABLE travel_briefs ADD COLUMN email_notifications BOOLEAN DEFAULT TRUE",
                'sms_notifications': "ALTER TABLE travel_briefs ADD COLUMN sms_notifications BOOLEAN DEFAULT FALSE"
            }
            
            # Add missing columns
            for col_name, sql in required_columns.items():
                if col_name not in columns:
                    try:
                        db.session.execute(text(sql))
                        db.session.commit()
                        print(f"✅ Added column: {col_name}")
                    except Exception as e:
                        db.session.rollback()
                        error_msg = str(e).lower()
                        if "duplicate" in error_msg or "already exists" in error_msg:
                            print(f"ℹ️  Column already exists: {col_name}")
                        else:
                            print(f"❌ Error adding {col_name}: {e}")
                else:
                    print(f"ℹ️  Column exists: {col_name}")
        
        print("\n✅ Migration completed successfully!")
        return True

if __name__ == '__main__':
    try:
        success = run_migration()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)