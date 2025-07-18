# Travel AiGent - AI Travel Deal Monitor

## Overview

Travel AiGent is an automated travel deal monitoring system built for the Lefley family. The system monitors travel briefs stored in Google Sheets, searches for deals through the Amadeus Travel API, analyzes deals using OpenAI, and sends alerts via Telegram when suitable deals are found.

The application consists of a Flask web interface for monitoring system status and a background scheduler that periodically searches for travel deals based on active briefs. The system is designed to be autonomous, running continuously to find and alert about travel opportunities that match the family's preferences and budget.

## System Architecture

### **Web Application Layer**
- **Flask Web Server**: Provides a dashboard interface for monitoring system status, active briefs, and deal statistics
- **RESTful API Endpoints**: Exposes system status, briefs data, and deal information
- **Static Assets**: HTML/CSS/JavaScript frontend for real-time monitoring

### **Background Processing Layer**
- **Scheduler Service**: Uses the `schedule` library to run deal searches every 6 hours
- **Travel Agent Core**: Orchestrates the entire deal discovery and analysis workflow
- **Parallel Execution**: Web server and scheduler run in parallel using threading

### **External Service Integration Layer**
- **Google Sheets**: Stores travel briefs and deal records
- **Amadeus Travel API**: Provides flight and hotel data
- **OpenAI API**: Analyzes deal suitability using AI
- **Telegram Bot**: Sends real-time alerts to family chat

## Key Components

### **Travel Agent (`travel_agent.py`)**
The central orchestrator that coordinates all system components. Manages the workflow of retrieving briefs, searching for deals, analyzing matches, and sending notifications. Tracks statistics and system health.

### **API Integrations**
- **Amadeus API Handler (`amadeus_api.py`)**: Manages OAuth authentication, rate limiting, and travel data retrieval
- **OpenAI Analyzer (`openai_analyzer.py`)**: Implements AI-powered deal analysis with scoring and recommendations
- **Sheets Handler (`sheets_handler.py`)**: Handles Google Sheets authentication and data operations using service account credentials

### **Notification System (`telegram_notifier.py`)**
Formats and sends rich travel deal alerts to Telegram, including deal scoring, pricing, and booking recommendations.

### **Configuration Management (`config.py`)**
Centralizes all environment variables, API keys, family profile data, and system settings. Includes rate limiting configurations and travel preferences.

### **Logging System (`logger.py`)**
Comprehensive logging with both console and file output, configurable log levels, and separate logging for different system components.

## Data Flow

1. **Brief Retrieval**: System reads active travel briefs from Google Sheets containing destinations, dates, budgets, and requirements
2. **Deal Search**: Amadeus API is queried for flights and accommodations matching brief criteria
3. **AI Analysis**: OpenAI analyzes each deal against family preferences, budget, and requirements, providing a suitability score
4. **Filtering**: Only deals scoring above the minimum threshold (8/10) proceed to notification
5. **Alert Generation**: High-scoring deals are formatted into rich Telegram messages and sent to the family chat
6. **Record Keeping**: Deal results are logged and statistics are updated for monitoring

## External Dependencies

### **Travel Data**
- **Amadeus for Developers API**: Flight searches, hotel availability, and pricing data
- **Rate Limiting**: 10 requests per minute with automatic token refresh

### **AI Analysis**
- **OpenAI GPT API**: Deal analysis and scoring with family-specific context
- **Rate Limiting**: 20 requests per minute with intelligent queuing

### **Data Storage**
- **Google Sheets API**: Travel briefs database with service account authentication
- **Local Logging**: File-based logs for troubleshooting and monitoring

### **Communication**
- **Telegram Bot API**: Real-time family notifications with rich formatting

## Deployment Strategy

### **Replit Environment**
- **Python 3.11 Runtime**: Using Nix package manager for dependencies
- **Parallel Workflow**: Web server (Flask) and scheduler run simultaneously
- **Port Configuration**: Flask serves on port 5000 with automatic port detection

### **Environment Variables**
Required secrets configuration:
- `AMADEUS_CLIENT_ID` / `AMADEUS_CLIENT_SECRET`
- `OPENAI_API_KEY`
- `TELEGRAM_BOT_TOKEN` / `TELEGRAM_CHAT_ID`
- `GOOGLE_SHEET_ID` / `GOOGLE_CREDENTIALS_JSON`

### **Family Profile Configuration**
Hard-coded family details in config.py:
- 2 adults + 2-3 children travel configurations
- London airports (LHR preferred)
- Age-specific pricing and requirements

### **Monitoring and Resilience**
- Comprehensive error handling with automatic retry logic
- Health check endpoints for system monitoring
- Graceful degradation when external services are unavailable
- Mock data fallbacks for development and testing

## Recent Changes

- **June 27, 2025 - Database Integration**: Added PostgreSQL database with comprehensive models for travel briefs, deals, and system statistics. Database tables automatically created and integrated with Flask app.

- **June 27, 2025 - Google Sheets Connection**: Successfully connected to real Google Sheets data. System now reads actual travel brief "TB-OCT-2025" with destinations including Barcelona, Valencia, Rome, etc. Updated worksheet names to match actual sheet structure.

- **June 27, 2025 - Real Data Processing**: System now processes authentic travel briefs from Google Sheets, logs deals with AI analysis, and updates timestamps. Successfully processing travel brief "TB-OCT-2025" with destinations across Europe.

- **June 27, 2025 - API Integration Status**: OpenAI and Telegram fully operational with real data. Google Sheets connected and processing authentic travel briefs. Amadeus API now fully operational with production credentials - successfully retrieving real flight data from 500+ airlines.

- **June 27, 2025 - Design Update**: Redesigned interface with Airbnb-inspired clean aesthetic. Updated branding to "Lefley TravelAiGent" with modern card layouts, elegant typography, and travel-focused design patterns.

- **June 27, 2025 - Curated Experience Implementation**: Transformed from raw deal display to premium travel package experience. System now only shows deals scoring 8+ with beautiful empty state when no qualified packages exist. Implemented destination-specific imagery, package-style presentation, and intelligent filtering to ensure only family-suitable options appear.

- **June 27, 2025 - Complete Travel Packages**: Enhanced Amadeus integration to search for both flights AND accommodation as combined packages. System now searches 4+ star family-friendly hotels only (as per brief requirements) using Amadeus Hotel API, creating complete travel experiences with flight+hotel combinations and package savings calculations.

- **June 27, 2025 - Interactive Brief Details**: Added clickable navigation from Active Briefs to detailed brief pages showing travel requirements, monitoring status, preferences, and action buttons. Enhanced user experience with colorful gradient panels and destination-specific visual elements.

- **June 27, 2025 - Vibrant Design Transformation**: Complete redesign with colorful gradients and modern glassmorphism effects. Added vibrant background gradients, gradient text effects on headings, transparent cards with backdrop blur, and colorful destination-specific gradients. Enhanced Active Briefs section with hover animations and premium travel package styling using glassmorphism design patterns.

- **June 28, 2025 - Live Amadeus Connection & UI Improvements**: Established live Amadeus API connection with successful authentication. System now retrieves real flight data from 500+ airlines across multiple London airports (LHR, LGW, STN) to European destinations. Fixed dashboard readability by changing headlines to white and panel numbers to sand-colored yellow. Implemented dynamic coloring - numbers turn green when deals found and alerts sent. Reduced deal check frequency from 6 hours to 1 hour for more responsive monitoring.

- **June 28, 2025 - Enhanced Accommodation Display & Notifications**: Created comprehensive accommodation viewing system with detailed hotel information including names, ratings, amenities, and room types. Added modal popup for full package details showing flight+hotel breakdown. Enhanced Telegram notifications to include brief ID and name at the top of each alert for clear identification of which travel brief triggered the notification.

## Changelog

- June 27, 2025. Initial setup with comprehensive Travel AiGent system

## User Preferences

Preferred communication style: Simple, everyday language.