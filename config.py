import os

# API Configuration
AMADEUS_CLIENT_ID = os.getenv("AMADEUS_CLIENT_ID", "")
AMADEUS_CLIENT_SECRET = os.getenv("AMADEUS_CLIENT_SECRET", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

# Google Sheets Configuration
GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID", "")
GOOGLE_CREDENTIALS_JSON = os.getenv("GOOGLE_CREDENTIALS_JSON", "")

# Application Settings
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
MAX_DEALS_PER_SEARCH = int(os.getenv("MAX_DEALS_PER_SEARCH", "20"))
MIN_SCORE_FOR_ALERT = int(os.getenv("MIN_SCORE_FOR_ALERT", "8"))
SEARCH_INTERVAL_HOURS = int(os.getenv("SEARCH_INTERVAL_HOURS", "1"))

# Family Configuration
FAMILY_PROFILE = {
    "adults": 2,
    "children_ages": [13, 10],
    "optional_teen": 17,
    "home_airports": ["LHR", "LGW", "STN"],
    "preferred_airport": "LHR",
    "base_location": "London, UK"
}

# Rate Limiting
AMADEUS_REQUESTS_PER_MINUTE = 10
OPENAI_REQUESTS_PER_MINUTE = 20
