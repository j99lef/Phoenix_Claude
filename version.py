"""Version information for TravelAiGent application."""
from datetime import datetime

# Semantic versioning: MAJOR.MINOR.PATCH
VERSION_MAJOR = 1
VERSION_MINOR = 2
VERSION_PATCH = 0

# Build metadata
BUILD_NUMBER = 12  # Increment with each build
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