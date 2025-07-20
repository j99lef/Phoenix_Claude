"""Version information for TravelAiGent application."""
from datetime import datetime

# Semantic versioning: MAJOR.MINOR.PATCH
VERSION_MAJOR = 1
VERSION_MINOR = 3
VERSION_PATCH = 10

# Build metadata
BUILD_NUMBER = 49  # Increment with each build
BUILD_DATE = datetime.now().strftime("%Y-%m-%d")
BUILD_TIME = datetime.now().strftime("%H:%M:%S")

# Version string
VERSION = f"{VERSION_MAJOR}.{VERSION_MINOR}.{VERSION_PATCH}"
VERSION_FULL = f"{VERSION}+build.{BUILD_NUMBER}"

# Feature flags for this version
VERSION_FEATURES = {
    "gmail_notifications": True,
    "password_reset": True,
    "whatsapp_notifications": False,  # Removed in v1.2.0
    "amadeus_integration": True,
    "deal_matching": True,
}

# Version history
VERSION_HISTORY = {
    "1.3.10": {
        "date": "2025-01-20",
        "changes": [
            "Fixed school holiday dropdown now properly shows when user has calendar configured",
            "Profile API now returns school calendar country from UserSchoolCalendar",
            "Profile API can now save/update school calendar country",
            "Removed redundant 'Focus on school holidays and INSET days' section",
            "School holiday dropdown loads holidays from user's calendar settings"
        ]
    },
    "1.3.9": {
        "date": "2025-01-20",
        "changes": [
            "Fixed button layout in School Calendar view mode",
            "Changed 'Save Changes' button to 'Edit Dates' with pencil icon",
            "Improved button visibility toggling for better UX",
            "Fixed state management after saving calendar changes",
            "Buttons now properly hide/show based on current mode"
        ]
    },
    "1.3.8": {
        "date": "2025-01-20",
        "changes": [
            "Fixed 'View School Dates' button formatting and renamed to 'Customise Dates'",
            "Fixed School Calendar flow - now prompts to create group after saving calendar",
            "Added school holiday dropdown to Travel Briefs page",
            "Shows prompt to add Travel Group if no school calendar configured",
            "School holidays can be selected from dropdown for quick date selection"
        ]
    },
    "1.3.7": {
        "date": "2025-01-20",
        "changes": [
            "Simplified School Calendar UI in Travel Groups page",
            "Added school holiday selector for travel briefs with children",
            "Toggle between holiday selection and custom dates",
            "Integrated travel groups with school calendar API",
            "Added API endpoints for group calendar data"
        ]
    },
    "1.3.6": {
        "date": "2025-01-20",
        "changes": [
            "Enhanced School Calendar Settings with full customization",
            "Added country-specific term dates with pre-populated defaults",
            "Added INSET days management for personal school dates",
            "Fixed validation error for travel brief creation",
            "Dynamic version display across all pages"
        ]
    },
    "1.3.5": {
        "date": "2025-01-20",
        "changes": [
            "Fixed Amadeus API integration - now finding real flights",
            "Added Amadeus API credentials to environment",
            "Fixed date parsing issues in travel brief processing",
            "Improved hotel search API calls",
            "Amadeus API now successfully searches London to Paris/Rome flights"
        ]
    },
    "1.3.0": {
        "date": "2025-01-20",
        "changes": [
            "Removed deals section to focus on AI travel brief searches",
            "Implemented UK school calendar system with holidays data",
            "Added country-based school calendar selection",
            "Added personal INSET days management", 
            "Integrated school holiday preferences in travel briefs",
            "Fixed travelers form to allow multiple people",
            "Simplified profile for better user experience"
        ]
    },
    "1.2.0": {
        "date": "2025-01-19",
        "changes": [
            "Replaced Twilio/SendGrid with Gmail SMTP",
            "Implemented password reset functionality",
            "Added password reset tokens table",
            "Removed WhatsApp notification dependencies",
            "Simplified email configuration"
        ]
    },
    "1.1.0": {
        "date": "2025-01-18",
        "changes": [
            "Added WhatsApp notifications via Twilio",
            "Implemented email notifications",
            "Fixed critical production issues",
            "Added deal search functionality",
            "Fixed authentication persistence"
        ]
    },
    "1.0.0": {
        "date": "2025-01-17",
        "changes": [
            "Initial release",
            "User registration and authentication",
            "Travel brief creation",
            "People profiles and groups",
            "Amadeus API integration",
            "Basic deal matching"
        ]
    }
}

def get_version_info():
    """Get complete version information as a dictionary."""
    return {
        "version": VERSION,
        "version_full": VERSION_FULL,
        "major": VERSION_MAJOR,
        "minor": VERSION_MINOR,
        "patch": VERSION_PATCH,
        "build": BUILD_NUMBER,
        "build_date": BUILD_DATE,
        "build_time": BUILD_TIME,
        "features": VERSION_FEATURES,
        "latest_changes": VERSION_HISTORY.get(VERSION, {}).get("changes", [])
    }

def get_version_string():
    """Get formatted version string for display."""
    return f"TravelAiGent v{VERSION_FULL} ({BUILD_DATE})"