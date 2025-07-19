"""Add WhatsApp number field to users table."""
from flask import Flask
from travel_aigent import create_app
from travel_aigent.models import db

def upgrade():
    """Add whatsapp_number column to users table."""
    app = create_app()
    
    with app.app_context():
        try:
            # Add WhatsApp number column
            db.engine.execute("""
                ALTER TABLE users 
                ADD COLUMN IF NOT EXISTS whatsapp_number VARCHAR(20)
            """)
            
            print("✅ Successfully added whatsapp_number column to users table")
            
        except Exception as e:
            print(f"❌ Error adding whatsapp_number column: {e}")
            # Column might already exist, which is fine
            if "already exists" not in str(e).lower():
                raise

if __name__ == "__main__":
    upgrade()