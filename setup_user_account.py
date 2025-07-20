#!/usr/bin/env python3
"""
Script to set up or update a proper user account with email for testing notifications
"""
import os
import sys
from werkzeug.security import generate_password_hash

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import app
from travel_aigent.models import db, User
from travel_aigent.services.notifications import notification_service

def setup_user_account():
    """Set up or update user account with full details"""
    with app.app_context():
        print("\n=== TravelAiGent User Account Setup ===\n")
        
        # Get username
        username = input("Enter username (default: admin): ").strip() or "admin"
        
        # Check if user exists
        user = User.query.filter_by(username=username).first()
        
        if user:
            print(f"\nUser '{username}' already exists. Updating details...")
            action = "updated"
        else:
            print(f"\nCreating new user '{username}'...")
            user = User(username=username)
            action = "created"
        
        # Get user details
        print("\nEnter user details (press Enter to keep existing values):")
        
        # Email (REQUIRED for notifications)
        while True:
            email = input(f"Email address{f' [{user.email}]' if user and user.email else ''}: ").strip()
            if email:
                user.email = email
                break
            elif user and user.email:
                break
            else:
                print("Email is required for notifications. Please enter an email address.")
        
        # Personal details
        first_name = input(f"First name{f' [{user.first_name}]' if user and user.first_name else ''}: ").strip()
        if first_name:
            user.first_name = first_name
        
        last_name = input(f"Last name{f' [{user.last_name}]' if user and user.last_name else ''}: ").strip()
        if last_name:
            user.last_name = last_name
        
        # Phone numbers
        phone = input(f"Phone number{f' [{user.phone}]' if user and user.phone else ''}: ").strip()
        if phone:
            user.phone = phone
        
        whatsapp = input(f"WhatsApp number (with country code){f' [{user.whatsapp_number}]' if user and user.whatsapp_number else ''}: ").strip()
        if whatsapp:
            user.whatsapp_number = whatsapp
        
        # Password (only for new users or if requested)
        if not user.id or input("\nUpdate password? (y/N): ").lower() == 'y':
            while True:
                password = input("Password (min 6 characters): ").strip()
                if len(password) >= 6:
                    user.password_hash = generate_password_hash(password)
                    break
                else:
                    print("Password must be at least 6 characters.")
        
        # Travel preferences
        print("\nTravel Preferences (optional):")
        
        home_airports = input(f"Home airports (e.g., LHR, LGW, STN){f' [{user.home_airports}]' if user and user.home_airports else ''}: ").strip()
        if home_airports:
            user.home_airports = home_airports
        
        # Enable email notifications
        user.preferences = '{"email_notifications": true}'
        
        # Save to database
        try:
            if not user.id:
                db.session.add(user)
            db.session.commit()
            
            print(f"\n✅ User account {action} successfully!")
            print(f"\nUser Details:")
            print(f"  Username: {user.username}")
            print(f"  Email: {user.email}")
            print(f"  Name: {user.first_name} {user.last_name}")
            print(f"  User ID: {user.id}")
            
            # Test email configuration
            print("\n=== Email Configuration Test ===")
            if notification_service.smtp_username:
                print(f"✅ Gmail configured: {notification_service.smtp_username}")
                
                # Send test email
                if input("\nSend test welcome email? (Y/n): ").lower() != 'n':
                    print(f"Sending test email to {user.email}...")
                    result = notification_service.send_welcome_message(user)
                    if result['email']:
                        print("✅ Test email sent successfully! Check your inbox.")
                    else:
                        print("❌ Failed to send test email. Check Gmail configuration.")
            else:
                print("❌ Gmail not configured. Set these environment variables:")
                print("   GMAIL_USERNAME=your-gmail@gmail.com")
                print("   GMAIL_APP_PASSWORD=your-app-specific-password")
                print("\nTo get an app password:")
                print("1. Go to https://myaccount.google.com/security")
                print("2. Enable 2-factor authentication")
                print("3. Generate an app-specific password")
            
            return user
            
        except Exception as e:
            print(f"\n❌ Error saving user: {e}")
            db.session.rollback()
            return None

def show_gmail_setup():
    """Show instructions for Gmail setup"""
    print("\n=== Gmail Setup Instructions ===")
    print("\n1. Enable 2-factor authentication on your Google account:")
    print("   https://myaccount.google.com/security")
    print("\n2. Generate an app-specific password:")
    print("   https://myaccount.google.com/apppasswords")
    print("\n3. Set environment variables on Railway:")
    print("   GMAIL_USERNAME=your-email@gmail.com")
    print("   GMAIL_APP_PASSWORD=xxxx-xxxx-xxxx-xxxx")
    print("\n4. Optional: Set custom FROM_EMAIL if different from GMAIL_USERNAME")
    print("\nNote: Regular Gmail passwords won't work - you must use an app password!")

if __name__ == "__main__":
    print("TravelAiGent User Account Setup")
    print("==============================")
    
    user = setup_user_account()
    
    if user:
        print("\n✅ Setup complete! You can now:")
        print("1. Log in with your username and password")
        print("2. Create travel briefs")
        print("3. Receive email notifications for matching deals")
        
        if not notification_service.smtp_username:
            show_gmail_setup()
    else:
        print("\n❌ Setup failed. Please check the error messages above.")