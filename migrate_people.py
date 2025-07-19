#!/usr/bin/env python
"""Migration script to add Person and GroupMember tables"""
import sys
from sqlalchemy import inspect
from travel_aigent import create_app
from travel_aigent.models import db, Person, GroupMember, TravelGroup

def migrate_database():
    """Add new tables for Person and GroupMember models"""
    app = create_app()
    
    with app.app_context():
        inspector = inspect(db.engine)
        existing_tables = inspector.get_table_names()
        
        # Check if tables already exist
        if 'people' in existing_tables:
            print("❗ 'people' table already exists")
        else:
            # Create new tables
            Person.__table__.create(db.engine)
            print("✅ Created 'people' table")
        
        if 'group_members' in existing_tables:
            print("❗ 'group_members' table already exists")
        else:
            GroupMember.__table__.create(db.engine)
            print("✅ Created 'group_members' table")
        
        # Add is_primary column to travel_groups if it doesn't exist
        if 'travel_groups' in existing_tables:
            columns = [col['name'] for col in inspector.get_columns('travel_groups')]
            if 'is_primary' not in columns:
                from sqlalchemy import text
                with db.engine.connect() as conn:
                    conn.execute(text('ALTER TABLE travel_groups ADD COLUMN is_primary BOOLEAN DEFAULT FALSE'))
                    conn.commit()
                print("✅ Added 'is_primary' column to travel_groups table")
            else:
                print("❗ 'is_primary' column already exists in travel_groups")
        
        print("\n✨ Database migration completed!")

if __name__ == "__main__":
    migrate_database()