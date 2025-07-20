#!/usr/bin/env python3
"""
Script to update database with new SearchActivity table
"""
import os
import sys
from sqlalchemy import text

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import app
from travel_aigent.models import db, SearchActivity

def update_database():
    """Create the SearchActivity table if it doesn't exist"""
    with app.app_context():
        try:
            # Check if table exists
            inspector = db.inspect(db.engine)
            if 'search_activities' not in inspector.get_table_names():
                print("Creating search_activities table...")
                
                # Create the table
                SearchActivity.__table__.create(db.engine)
                print("✓ search_activities table created successfully")
            else:
                print("✓ search_activities table already exists")
                
            # Verify table structure
            columns = [col['name'] for col in inspector.get_columns('search_activities')]
            print(f"Table columns: {columns}")
            
        except Exception as e:
            print(f"Error updating database: {e}")
            return False
    
    return True

if __name__ == "__main__":
    print("Updating database schema...")
    if update_database():
        print("Database update completed successfully!")
    else:
        print("Database update failed!")
        sys.exit(1)