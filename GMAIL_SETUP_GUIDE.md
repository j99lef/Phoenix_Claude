# Gmail Setup Guide for TravelAiGent Email Notifications

## Overview
TravelAiGent sends email notifications when it finds travel deals matching your criteria. To enable this, you need to configure Gmail with an app-specific password.

## Step 1: Update Your User Account with Email

Run this command with your email address:
```bash
python3 update_admin_email.py your-email@gmail.com
```

## Step 2: Enable 2-Factor Authentication on Gmail

1. Go to [Google Account Security](https://myaccount.google.com/security)
2. Click on "2-Step Verification"
3. Follow the prompts to enable it (if not already enabled)

## Step 3: Generate App-Specific Password

1. Go to [App Passwords](https://myaccount.google.com/apppasswords)
2. Select "Mail" from the dropdown
3. Select "Other" for device
4. Enter "TravelAiGent" as the name
5. Click "Generate"
6. Copy the 16-character password (looks like: xxxx xxxx xxxx xxxx)

## Step 4: Configure Railway Environment Variables

1. Go to your Railway dashboard
2. Click on your TravelAiGent service
3. Go to "Variables" tab
4. Add these variables:

```
GMAIL_USERNAME=your-email@gmail.com
GMAIL_APP_PASSWORD=xxxxxxxxxxxxxxxx
```

**Important**: Enter the app password WITHOUT spaces

Optional:
```
FROM_EMAIL=noreply@travelaigent.com
```

## Step 5: Verify Setup

Railway will automatically redeploy. After deployment:

1. Create a new travel brief
2. Check the brief detail page for search activity
3. When a deal is found with score 8+, you'll receive an email

## Email Notification Details

### What Triggers Emails
- Deal match score of 8/10 or higher
- Based on your brief criteria:
  - Budget match
  - Date match
  - Destination match
  - Family suitability

### Email Content
- Deal title and description
- Price with savings percentage
- Direct booking link
- Match score explanation
- Travel dates and destination

### Frequency
- Immediate: When brief is created
- Recurring: Every 6 hours
- Manual: When you click "Trigger New Search"

## Troubleshooting

### Not Receiving Emails?

1. **Check Spam Folder**: First emails might go to spam
2. **Verify Email in Profile**: Go to /profile and check email is correct
3. **Check Brief Settings**: Ensure "Email notifications" is ON
4. **Check Railway Logs**: Look for email sending errors
5. **Test Email**: Run `python3 test_email.py` locally

### Common Issues

**"Gmail credentials not configured"**
- Environment variables not set on Railway
- Variables have typos
- App password includes spaces

**"Failed to send email"**
- Wrong app password
- 2FA not enabled
- Using regular password instead of app password

**"No email address for user"**
- User account missing email
- Run update_admin_email.py again

## Security Notes

- App passwords are specific to TravelAiGent
- They can be revoked anytime from Google Account
- Don't share your app password
- Use environment variables, never hardcode

## Next Steps

Once configured:
1. Create travel briefs with your destinations
2. Set your budget and dates
3. Wait for deal notifications
4. Click booking links in emails to book directly

## Support

If you need help:
1. Check Railway logs for errors
2. Verify all steps were followed
3. Try sending a test notification from the brief page