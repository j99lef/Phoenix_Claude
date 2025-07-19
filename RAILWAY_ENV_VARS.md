# Railway Environment Variables Setup

## Required Environment Variables

Add these environment variables to your Railway deployment:

### 1. Amadeus API (Travel Deal Search)
```
AMADEUS_CLIENT_ID=xNIE44DrMfsiRPXpLCXG7EzjOxntDGAf
AMADEUS_CLIENT_SECRET=GYJGY2FW7pkohsQx
```

### 2. Flask Configuration
```
FLASK_SECRET_KEY=your-secure-secret-key-here
FLASK_ENV=production
```

### 3. Database (Railway provides this automatically)
```
DATABASE_URL=postgresql://...
```

### 4. Email Notifications (Gmail)
```
GMAIL_USERNAME=your-email@gmail.com
GMAIL_APP_PASSWORD=your-app-specific-password
```

### 5. Optional: Telegram Notifications
```
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
```

## How to Add Environment Variables on Railway

1. Go to your Railway project dashboard
2. Click on your deployment (phoenixclaude)
3. Go to the "Variables" tab
4. Click "Add Variable"
5. Add each variable name and value
6. Railway will automatically redeploy with the new variables

## Testing Amadeus API

Once you've added the credentials, the app will:
- Automatically search for flight deals matching your travel briefs
- Display deals with match scores in your deals list
- Send notifications when new deals are found (if configured)

## Important Security Note

⚠️ Never commit these credentials to your repository. Always use environment variables for sensitive data.