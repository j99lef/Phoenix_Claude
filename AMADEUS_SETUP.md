# Amadeus API Setup and Deal Notifications

## Current Status

The Amadeus API integration is partially implemented but requires configuration:

### 1. **API Credentials**
To enable Amadeus API functionality, you need to:
1. Sign up for an Amadeus developer account at https://developers.amadeus.com
2. Create an app and get your API credentials
3. Set these environment variables on Railway:
   - `AMADEUS_CLIENT_ID`
   - `AMADEUS_CLIENT_SECRET`

### 2. **How Deal Search Works**
- When you create a travel brief, the system stores your preferences
- The background scheduler (if enabled) periodically searches for deals matching your briefs
- Deals are matched based on:
  - Destination
  - Travel dates
  - Budget
  - Group size
  - Accommodation preferences

### 3. **Notification System**
Currently implemented notification methods:
- **In-app notifications**: Deals appear in your deals list when found
- **Email notifications**: Not yet implemented (requires email service setup)
- **Telegram notifications**: Partially implemented (requires Telegram bot setup)

### 4. **To Enable Notifications**

#### Email Notifications
1. Set up an email service (SendGrid, AWS SES, etc.)
2. Add environment variables:
   - `EMAIL_SERVICE=sendgrid`
   - `SENDGRID_API_KEY=your-key`
   - `FROM_EMAIL=noreply@yourdomain.com`

#### Telegram Notifications
1. Create a Telegram bot via @BotFather
2. Set environment variables:
   - `TELEGRAM_BOT_TOKEN=your-bot-token`
3. Users need to start a chat with your bot and save their chat ID

### 5. **Manual Deal Search**
Without Amadeus API credentials, you can still:
- Manually add deals using the "Add Deal" feature
- Search existing deals in the database
- The system will still match deals to your travel briefs

### 6. **Testing Deal Matching**
To test if deals are being found:
1. Create a travel brief with specific criteria
2. Add a test deal that matches those criteria
3. Check if the deal appears in your deals list with a match score

## Next Steps

1. **Enable Amadeus API**: Add credentials to Railway environment variables
2. **Set up notifications**: Choose email or Telegram and configure
3. **Enable scheduler**: The background job scheduler needs to be running to automatically search for deals

The system is designed to work as a deal finder that redirects you to booking sites, not as a booking platform itself.