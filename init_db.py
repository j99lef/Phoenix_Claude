#!/usr/bin/env python3
"""Initialize or update database schema."""

import os
import sys
from travel_aigent import create_app
from travel_aigent.models import db

def init_database():
    """Initialize database with all tables."""
    app = create_app()
    
    with app.app_context():
        # Create all tables
        db.create_all()
        print("✅ Database tables created successfully!")
        
        # Check if tables exist
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        
        print("\n📊 Existing tables:")
        for table in tables:
            print(f"  - {table}")
            
        # Check for new columns in travel_briefs table
        if 'travel_briefs' in tables:
            columns = [col['name'] for col in inspector.get_columns('travel_briefs')]
            print(f"\n📋 Columns in travel_briefs: {', '.join(columns)}")
            
            # Check for new columns
            new_columns = ['status', 'last_deal_check', 'deal_notifications', 
                          'email_notifications', 'sms_notifications']
            missing = [col for col in new_columns if col not in columns]
            
            if missing:
                print(f"\n⚠️  Missing columns in travel_briefs: {', '.join(missing)}")
                print("You may need to manually add these columns or recreate the table.")
        
        # Check if deals table exists
        if 'deals' not in tables:
            print("\n⚠️  'deals' table not found - it should have been created")
        
        # Check if user_schools table exists  
        if 'user_schools' not in tables:
            print("\n⚠️  'user_schools' table not found - it should have been created")

if __name__ == '__main__':
    try:
        init_database()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)