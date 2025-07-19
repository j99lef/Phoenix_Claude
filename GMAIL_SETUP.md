# Gmail Email Setup Guide

This guide explains how to set up Gmail for sending email notifications in TravelAiGent.

## Prerequisites

1. A Gmail account
2. 2-factor authentication enabled on your Gmail account
3. An app-specific password for Gmail

## Setting Up Gmail App Password

1. Go to your Google Account settings: https://myaccount.google.com/
2. Navigate to "Security"
3. Under "Signing in to Google", ensure 2-Step Verification is ON
4. Click on "2-Step Verification"
5. Scroll to the bottom and click on "App passwords"
6. Select "Mail" as the app and your device type
7. Click "Generate"
8. Copy the 16-character password (spaces included)

## Environment Variables

Add these to your `.env` file or Railway environment variables:

```bash
# Gmail Configuration
GMAIL_USERNAME=your-email@gmail.com
GMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx  # Your 16-character app password with spaces

# Optional - defaults to Gmail settings
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
FROM_EMAIL=your-email@gmail.com  # Defaults to GMAIL_USERNAME if not set
```

## Testing the Setup

Run the test script to verify your Gmail configuration:

```bash
python test_gmail.py
```

Enter a test email address when prompted. You should receive a test email if everything is configured correctly.

## Production Deployment

For Railway deployment:

1. Go to your Railway project settings
2. Navigate to "Variables"
3. Add the following variables:
   - `GMAIL_USERNAME`: Your Gmail address
   - `GMAIL_APP_PASSWORD`: Your app-specific password (with spaces)

## Troubleshooting

### Common Issues:

1. **Authentication Failed**
   - Ensure 2-factor authentication is enabled
   - Verify the app password is correct (including spaces)
   - Check that "Less secure app access" is not blocking the connection

2. **Connection Timeout**
   - Verify your network allows outbound SMTP connections on port 587
   - Some corporate networks may block SMTP ports

3. **Email Not Received**
   - Check spam/junk folder
   - Verify the recipient email is correct
   - Check Gmail's sending limits (500 emails/day for regular accounts)

## Security Notes

- Never commit your Gmail password or app password to version control
- Use environment variables for all sensitive credentials
- Consider using a dedicated Gmail account for your application
- Monitor your Gmail account for unusual activity

## Email Features

The notification service supports:
- HTML and plain text emails
- Welcome messages for new users
- Deal notification emails with rich formatting
- Automatic fallback to plain text for older email clients