"""Notification service for sending deal alerts via email."""
import os
import logging
from typing import Optional, Dict, Any
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class NotificationService:
    """Handles sending notifications via email and WhatsApp."""
    
    def __init__(self):
        """Initialize notification service with Gmail configuration."""
        # Gmail SMTP configuration
        self.smtp_host = os.environ.get('SMTP_HOST', 'smtp.gmail.com')
        self.smtp_port = int(os.environ.get('SMTP_PORT', 587))
        self.smtp_username = os.environ.get('GMAIL_USERNAME')  # Your Gmail address
        self.smtp_password = os.environ.get('GMAIL_APP_PASSWORD')  # App-specific password
        self.from_email = os.environ.get('FROM_EMAIL', self.smtp_username)
        
        # Validate configuration
        if not all([self.smtp_username, self.smtp_password]):
            logging.warning("Gmail credentials not configured. Email notifications will be disabled.")
        else:
            logging.info(f"Gmail notification service configured for {self.smtp_username}")
    
    
    def send_deal_notification(self, user: Any, deal: Any, brief: Any) -> Dict[str, bool]:
        """Send deal notification via email.
        
        Returns dict with status for email attempt.
        """
        results = {
            'email': False
        }
        
        # Prepare notification content
        subject = f"🎯 New Travel Deal: {deal.destination} - Save {deal.discount_percentage}%!"
        
        html_content = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <h2 style="color: #C9A96E;">New Travel Deal Match!</h2>
            
            <div style="background: #f5f5f5; padding: 20px; border-radius: 10px; margin: 20px 0;">
                <h3 style="color: #2C2C2C; margin-top: 0;">{deal.title}</h3>
                <p style="color: #666; font-size: 16px;">{deal.description}</p>
                
                <div style="margin: 20px 0;">
                    <span style="font-size: 24px; color: #C9A96E; font-weight: bold;">
                        £{deal.price}
                    </span>
                    <span style="text-decoration: line-through; color: #999; margin-left: 10px;">
                        £{deal.original_price}
                    </span>
                    <span style="background: #4CAF50; color: white; padding: 5px 10px; border-radius: 20px; margin-left: 10px;">
                        Save {deal.discount_percentage}%
                    </span>
                </div>
                
                <ul style="color: #666;">
                    <li><strong>Destination:</strong> {deal.destination}</li>
                    <li><strong>Travel Dates:</strong> {deal.departure_date.strftime('%d %b %Y')} - {deal.return_date.strftime('%d %b %Y')}</li>
                    <li><strong>Match Score:</strong> {deal.match_score}%</li>
                    {f'<li><strong>Hotel:</strong> {deal.hotel_name} ({deal.hotel_rating} stars)</li>' if deal.hotel_name else ''}
                </ul>
                
                <a href="{deal.booking_url}" style="display: inline-block; background: #C9A96E; color: white; padding: 12px 30px; text-decoration: none; border-radius: 25px; margin-top: 20px;">
                    Book Now
                </a>
            </div>
            
            <p style="color: #666; font-size: 14px;">
                This deal was found based on your travel brief: <strong>{brief.departure_location} to {brief.destination}</strong>
            </p>
            
            <hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">
            
            <p style="color: #999; font-size: 12px; text-align: center;">
                You received this email because you have an active travel brief with TravelAiGent.
                <br>
                <a href="https://travelaigent.com/briefs" style="color: #C9A96E;">Manage your travel briefs</a>
            </p>
        </div>
        """
        
        text_content = f"""
        New Travel Deal Match!
        
        {deal.title}
        {deal.description}
        
        Price: £{deal.price} (was £{deal.original_price}) - Save {deal.discount_percentage}%
        Destination: {deal.destination}
        Travel Dates: {deal.departure_date.strftime('%d %b %Y')} - {deal.return_date.strftime('%d %b %Y')}
        Match Score: {deal.match_score}%
        
        Book now: {deal.booking_url}
        
        This deal was found based on your travel brief: {brief.departure_location} to {brief.destination}
        """
        
        # Send email notification
        if user.email:
            results['email'] = self.send_email(
                to_email=user.email,
                subject=subject,
                html_content=html_content,
                text_content=text_content
            )
        else:
            logging.warning(f"No email address for user {user.id}")
        
        return results
    
    def send_email(self, to_email: str, subject: str, html_content: str, 
                   text_content: Optional[str] = None) -> bool:
        """Send email using Gmail SMTP."""
        if not all([self.smtp_username, self.smtp_password]):
            logging.error("Gmail credentials not configured")
            return False
            
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.from_email
            msg['To'] = to_email
            
            # Add text and HTML parts
            if text_content:
                msg.attach(MIMEText(text_content, 'plain'))
            msg.attach(MIMEText(html_content, 'html'))
            
            # Send email via Gmail
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)
            
            logging.info(f"Email sent successfully to {to_email} via Gmail")
            return True
            
        except Exception as e:
            logging.error(f"Failed to send email to {to_email}: {e}")
            return False
    
    
    def send_welcome_message(self, user: Any) -> Dict[str, bool]:
        """Send welcome message to new user."""
        subject = "Welcome to TravelAiGent! 🌟"
        
        html_content = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <h2 style="color: #C9A96E;">Welcome to TravelAiGent, {user.first_name or 'Traveler'}!</h2>
            
            <p style="color: #666; font-size: 16px; line-height: 1.6;">
                Your personal AI travel concierge is ready to find extraordinary deals tailored just for you.
            </p>
            
            <div style="background: #f5f5f5; padding: 20px; border-radius: 10px; margin: 20px 0;">
                <h3 style="color: #2C2C2C;">Getting Started:</h3>
                <ol style="color: #666; line-height: 1.8;">
                    <li>Create your first travel brief with your dream destination</li>
                    <li>Our AI will continuously search for matching deals</li>
                    <li>Receive instant notifications when we find great opportunities</li>
                    <li>Book directly with trusted partners at exclusive prices</li>
                </ol>
            </div>
            
            <a href="https://travelaigent.com/brief/new" style="display: inline-block; background: #C9A96E; color: white; padding: 12px 30px; text-decoration: none; border-radius: 25px; margin: 20px 0;">
                Create Your First Brief
            </a>
            
            <p style="color: #999; font-size: 14px;">
                Questions? Reply to this email and our team will help you get started.
            </p>
        </div>
        """
        
        text_content = f"""
        Welcome to TravelAiGent, {user.first_name or 'Traveler'}!
        
        Your personal AI travel concierge is ready to find extraordinary deals tailored just for you.
        
        Getting Started:
        1. Create your first travel brief with your dream destination
        2. Our AI will continuously search for matching deals
        3. Receive instant notifications when we find great opportunities
        4. Book directly with trusted partners at exclusive prices
        
        Create your first brief: https://travelaigent.com/brief/new
        
        Questions? Reply to this email and our team will help you get started.
        """
        
        results = {'email': False}
        
        if user.email:
            results['email'] = self.send_email(
                to_email=user.email,
                subject=subject,
                html_content=html_content,
                text_content=text_content
            )
        
        return results


# Global notification service instance
notification_service = NotificationService()