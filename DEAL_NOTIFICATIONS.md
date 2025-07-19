# Deal Notifications System

## How TravelAiGent Notifies You About Deals

### Current Implementation

TravelAiGent is designed to monitor for travel deals matching your briefs and notify you when great opportunities are found. Here's how it works:

## 1. **Continuous Monitoring**
When you create a travel brief, the system:
- Stores your search criteria
- Marks the brief as "active" 
- The AI agent periodically searches for matching deals
- New deals are saved with a `notification_sent = False` flag

## 2. **Notification Channels**

### Email Notifications (Requires Configuration)
To enable email notifications, add these environment variables in Railway:
```
EMAIL_SERVICE=sendgrid
SENDGRID_API_KEY=your-sendgrid-api-key
FROM_EMAIL=noreply@yourdomain.com
```

### Telegram Notifications (Optional)
For instant notifications via Telegram:
```
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
```

### In-App Notifications
- New deals appear in your deals list with a "NEW" badge
- Dashboard shows count of unread deals
- Deal match scores help prioritize the best opportunities

## 3. **How to See Your Notifications**

### Immediate Actions:
1. **Check Deals Page** - Go to /deals to see all matched deals
2. **View Travel Briefs** - Each brief shows how many deals were found
3. **Dashboard Stats** - Shows total deals and new opportunities

### Deal Information Displayed:
- Match score (how well it fits your criteria)
- Price and savings percentage
- Destination and dates
- Hotel rating and amenities
- Direct booking links

## 4. **Setting Up Notifications**

### For Production Deployment:

1. **Create SendGrid Account** (Free tier available)
   - Sign up at https://sendgrid.com
   - Create an API key
   - Verify your sender email

2. **Add to Railway Environment**:
   ```
   EMAIL_SERVICE=sendgrid
   SENDGRID_API_KEY=SG.xxxxxxxxxxxxx
   FROM_EMAIL=deals@yourdomain.com
   ```

3. **Optional: Telegram Setup**
   - Create a bot via @BotFather on Telegram
   - Get your bot token
   - Add to Railway: `TELEGRAM_BOT_TOKEN=xxxxx`

## 5. **How the Search Works**

The system searches for deals through:
1. **Amadeus API Integration** - Real-time flight and hotel inventory
2. **Price Monitoring** - Tracks price drops and special offers
3. **Match Scoring** - AI scores each deal based on your preferences
4. **Smart Filtering** - Only shows deals meeting your criteria

## 6. **Testing Your Setup**

To verify notifications are working:
1. Create a travel brief with popular destinations (Paris, Barcelona, Dubai)
2. Click "Search Deals Now" on the deals page
3. Check for new deals in your list
4. If email is configured, you'll receive notifications for high-scoring matches

## 7. **Notification Frequency**

- Searches run periodically (configurable, default every few hours)
- You're notified only for deals scoring 70% or higher match
- Each deal is notified only once to avoid spam
- Brief remains active until you pause or delete it

## 8. **Managing Notifications**

- **Pause a Brief**: Stop searching without deleting criteria
- **Delete a Brief**: Remove completely and stop all notifications
- **Mark as Read**: Clear the "NEW" badge on deals
- **Hide Deals**: Remove deals you're not interested in

## Next Steps

While email/Telegram require external services, the core notification system is working:
- New deals are tracked in the database
- Match scores help identify best opportunities  
- The deals page shows all your personalized recommendations
- Everything is ready to connect to your preferred notification service

To get started, create a travel brief and let TravelAiGent start finding your perfect deals!