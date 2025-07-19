"""Add WhatsApp number field to users table."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask
from travel_aigent import create_app
from travel_aigent.models import db
from sqlalchemy import text

def upgrade():
    """Add whatsapp_number column to users table."""
    app = create_app()
    
    with app.app_context():
        try:
            # Check if column already exists
            with db.engine.connect() as conn:
                result = conn.execute(text("PRAGMA table_info(users)"))
                columns = [row[1] for row in result]
                
                if 'whatsapp_number' in columns:
                    print("✅ whatsapp_number column already exists in users table")
                    return
                
                # Add WhatsApp number column
                conn.execute(text("""
                    ALTER TABLE users 
                    ADD COLUMN whatsapp_number VARCHAR(20)
                """))
                conn.commit()
            
            print("✅ Successfully added whatsapp_number column to users table")
            
        except Exception as e:
            print(f"❌ Error adding whatsapp_number column: {e}")
            # Column might already exist, which is fine
            if "duplicate column" in str(e).lower():
                print("✅ whatsapp_number column already exists")
            else:
                raise

if __name__ == "__main__":
    upgrade()