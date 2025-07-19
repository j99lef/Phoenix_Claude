#!/usr/bin/env python3
"""Test Gmail email sending functionality."""
import os
import sys
from datetime import datetime

# Set environment variables for testing
os.environ['GMAIL_USERNAME'] = 'phoenixtradingbotj99@gmail.com'
os.environ['GMAIL_APP_PASSWORD'] = 'muup exja ujxs vrmw'

# Import after setting env vars
from travel_aigent.services.notifications import notification_service

def test_email_sending(recipient_email="travelaigent@campley.uk"):
    """Test sending a simple email via Gmail."""
    print("Testing Gmail email sending...")
    print(f"Sending test email to: {recipient_email}")
    
    # Test email details
    test_email = recipient_email
    
    # Send test email
    result = notification_service.send_email(
        to_email=test_email,
        subject=f"TravelAiGent Gmail Test - {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        html_content="""
        <div style="font-family: Arial, sans-serif; padding: 20px;">
            <h2 style="color: #C9A96E;">Gmail Integration Test</h2>
            <p>This is a test email from TravelAiGent to verify Gmail SMTP is working correctly.</p>
            <p style="color: #666;">If you received this email, the Gmail integration is successful!</p>
            <hr style="border: none; border-top: 1px solid #eee; margin: 20px 0;">
            <p style="font-size: 12px; color: #999;">Sent via Gmail SMTP</p>
        </div>
        """,
        text_content="This is a test email from TravelAiGent. Gmail integration is working!"
    )
    
    if result:
        print("✅ Email sent successfully!")
    else:
        print("❌ Failed to send email. Check the logs for details.")
    
    return result

if __name__ == "__main__":
    import sys
    email = sys.argv[1] if len(sys.argv) > 1 else "travelaigent@campley.uk"
    test_email_sending(email)