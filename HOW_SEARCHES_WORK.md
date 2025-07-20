# How TravelAiGent Searches Work

## Search Schedule
- **Immediate search**: Runs automatically when you submit a new brief
- **Recurring searches**: Run every 6 hours after that
- **Manual trigger**: Available on each brief detail page anytime

## How to See Results

### 1. Brief Detail Page
- Go to "Travel Briefs" and click on your brief
- You'll see:
  - **Search Activity Timeline**: Shows all search attempts
  - **Discovered Deals**: Shows any deals found
  - **Activity Stats**: Shows hours active, estimated scans

### 2. Dashboard
- The main dashboard shows recent deals across all briefs
- Look for your destination in the deals list

### 3. Manual Search Trigger
- On any brief detail page, click "Trigger New Search"
- This runs an immediate search for that specific brief

## Notifications

### Email Notifications
- Sent when high-score deals (8/10 or higher) are found
- Check your email settings in Profile

### WhatsApp Notifications (if configured)
- Sent via Twilio for high-score deals
- Requires WhatsApp number in profile

### In-App Notifications
- Green success messages when searches complete
- Deal count updates on dashboard

## Why You Might Not See Results Yet

1. **Timing**: Searches run every 6 hours, so it might not have run yet
2. **No matching deals**: Amadeus API might not have deals matching your criteria
3. **API limits**: Free tier has limited searches per month
4. **Specific destinations**: Some destinations have fewer available deals

## How to Test If It's Working

1. Go to your brief detail page
2. Click "Trigger New Search" 
3. Check the Search Activity timeline - you should see a new entry
4. If using mock data (no Amadeus API), you'll see sample deals
5. With Amadeus API, results depend on actual availability

## Troubleshooting

- Check brief detail page for search activity
- Look for error messages in the timeline
- Verify your departure/return dates are in the future
- Try broader destinations (e.g., "Europe" instead of specific city)
- Check that your budget range is realistic for the destination