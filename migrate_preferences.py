"""Add preferences column to users table"""
from travel_aigent import create_app
from travel_aigent.models import db
import logging

logging.basicConfig(level=logging.INFO)

def add_preferences_column():
    """Add preferences column to users table if it doesn't exist"""
    app = create_app()
    
    with app.app_context():
        try:
            # Check if column exists
            result = db.session.execute(
                "SELECT column_name FROM information_schema.columns "
                "WHERE table_name='users' AND column_name='preferences'"
            )
            
            if not result.fetchone():
                # Add preferences column
                db.session.execute(
                    "ALTER TABLE users ADD COLUMN preferences TEXT DEFAULT '{\"email_notifications\": true}'"
                )
                db.session.commit()
                logging.info("Successfully added preferences column to users table")
            else:
                logging.info("Preferences column already exists")
                
        except Exception as e:
            logging.error(f"Error adding preferences column: {e}")
            db.session.rollback()

if __name__ == "__main__":
    add_preferences_column()