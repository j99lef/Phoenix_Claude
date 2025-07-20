#!/usr/bin/env python3
"""
Script to update database with new SearchActivity table and missing columns
"""
import os
import sys
from sqlalchemy import text

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import app
from travel_aigent.models import db, SearchActivity, TravelBrief

def update_database():
    """Create the SearchActivity table and add missing columns"""
    with app.app_context():
        try:
            inspector = db.inspect(db.engine)
            
            # Check if search_activities table exists
            if 'search_activities' not in inspector.get_table_names():
                print("Creating search_activities table...")
                SearchActivity.__table__.create(db.engine)
                print("✓ search_activities table created successfully")
            else:
                print("✓ search_activities table already exists")
            
            # Check for missing columns in travel_briefs table
            brief_columns = [col['name'] for col in inspector.get_columns('travel_briefs')]
            
            # Add missing columns to travel_briefs
            if 'focus_on_school_holidays' not in brief_columns:
                print("Adding focus_on_school_holidays column to travel_briefs...")
                db.session.execute(text(
                    "ALTER TABLE travel_briefs ADD COLUMN focus_on_school_holidays BOOLEAN DEFAULT 0"
                ))
                db.session.commit()
                print("✓ Added focus_on_school_holidays column")
            
            if 'preferred_holiday_periods' not in brief_columns:
                print("Adding preferred_holiday_periods column to travel_briefs...")
                db.session.execute(text(
                    "ALTER TABLE travel_briefs ADD COLUMN preferred_holiday_periods TEXT"
                ))
                db.session.commit()
                print("✓ Added preferred_holiday_periods column")
                
            # Verify table structures
            print("\nDatabase schema updated:")
            print(f"- search_activities columns: {[col['name'] for col in inspector.get_columns('search_activities')]}")
            print(f"- travel_briefs has school columns: {'focus_on_school_holidays' in [col['name'] for col in inspector.get_columns('travel_briefs')]}")
            
        except Exception as e:
            print(f"Error updating database: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    return True

if __name__ == "__main__":
    print("Updating database schema...")
    if update_database():
        print("\nDatabase update completed successfully!")
    else:
        print("\nDatabase update failed!")
        sys.exit(1)