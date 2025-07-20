#!/usr/bin/env python3
"""
Script to update admin account with email for notifications
"""
import os
import sys

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import app
from travel_aigent.models import db, User

def update_admin_email(email_address):
    """Update admin user with email address"""
    with app.app_context():
        # Get admin user
        user = User.query.filter_by(username='admin').first()
        
        if not user:
            print("❌ Admin user not found!")
            return False
        
        print(f"Found admin user (ID: {user.id})")
        
        # Update email
        user.email = email_address
        
        # Ensure email notifications are enabled
        user.preferences = '{"email_notifications": true}'
        
        # Update other fields if empty
        if not user.first_name:
            user.first_name = "Admin"
        
        try:
            db.session.commit()
            print(f"✅ Updated admin user with email: {email_address}")
            print(f"\nUser details:")
            print(f"  ID: {user.id}")
            print(f"  Username: {user.username}")
            print(f"  Email: {user.email}")
            print(f"  Name: {user.first_name} {user.last_name or ''}")
            print(f"  Notifications: Enabled")
            return True
        except Exception as e:
            print(f"❌ Error updating user: {e}")
            db.session.rollback()
            return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python update_admin_email.py <email_address>")
        print("Example: python update_admin_email.py your-email@gmail.com")
        sys.exit(1)
    
    email = sys.argv[1]
    if '@' not in email:
        print("❌ Invalid email address")
        sys.exit(1)
    
    print(f"Updating admin account with email: {email}")
    
    if update_admin_email(email):
        print("\n✅ Success! Now configure Gmail on Railway:")
        print("\n1. Go to Railway dashboard > Variables")
        print("2. Add these environment variables:")
        print("   GMAIL_USERNAME=your-gmail@gmail.com")
        print("   GMAIL_APP_PASSWORD=your-16-char-app-password")
        print("\n3. To get an app password:")
        print("   - Go to https://myaccount.google.com/apppasswords")
        print("   - Create a new app password for 'Mail'")
        print("   - Copy the 16-character password (without spaces)")
        print("\n4. Railway will automatically redeploy with email enabled")
    else:
        print("\n❌ Failed to update admin email")