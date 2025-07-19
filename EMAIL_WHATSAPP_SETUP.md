# Email & WhatsApp Notifications Setup Guide

## Overview

TravelAiGent now supports sending deal notifications via:
- **Email** (SendGrid or SMTP)
- **WhatsApp** (via Twilio)

## Email Setup

### Option 1: SendGrid (Recommended for Production)

1. **Create SendGrid Account**
   - Go to https://sendgrid.com/free/
   - Sign up for free tier (100 emails/day free)
   
2. **Get API Key**
   - Go to Settings → API Keys
   - Click "Create API Key"
   - Choose "Full Access"
   - Copy the key (starts with `SG.`)

3. **Verify Sender**
   - Go to Settings → Sender Authentication
   - Add and verify your sender email address

4. **Add to Railway**
   ```
   SENDGRID_API_KEY=SG.xxxxxxxxxxxxxxxxxxxxx
   FROM_EMAIL=deals@yourdomain.com
   ```

### Option 2: SMTP (Gmail Example)

1. **Enable 2-Factor Authentication** on your Gmail account

2. **Create App Password**
   - Go to https://myaccount.google.com/apppasswords
   - Select "Mail" and generate password

3. **Add to Railway**
   ```
   SMTP_HOST=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USERNAME=your-email@gmail.com
   SMTP_PASSWORD=your-app-password
   FROM_EMAIL=your-email@gmail.com
   ```

## WhatsApp Setup (via Twilio)

1. **Create Twilio Account**
   - Go to https://www.twilio.com/try-twilio
   - Sign up for free trial ($15 credit)

2. **Get WhatsApp Sandbox** (for testing)
   - In Twilio Console, go to Messaging → Try it out → Send a WhatsApp message
   - Follow instructions to join sandbox
   - Note the sandbox number (e.g., +14155238886)

3. **Get Credentials**
   - Find Account SID and Auth Token in console dashboard

4. **Add to Railway**
   ```
   TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxx
   TWILIO_AUTH_TOKEN=xxxxxxxxxxxxxxxxxx
   TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
   ```

5. **For Production** (optional)
   - Apply for WhatsApp Business API access
   - Get dedicated WhatsApp number
   - Requires business verification

## User Setup

### For Users to Receive Notifications:

1. **Email**: Automatically uses their registered email address

2. **WhatsApp**: 
   - Users add their WhatsApp number in Profile settings
   - Format: International format with country code (e.g., +44 7700 900123)
   - For Twilio Sandbox: Users must first join sandbox by sending message

## Testing Notifications

1. **Test Email/WhatsApp**
   ```bash
   curl -X POST https://yourdomain.com/api/notifications/test \
     -H "Cookie: session=your-session-cookie"
   ```

2. **Send Pending Notifications**
   ```bash
   curl https://yourdomain.com/api/notifications/send-pending \
     -H "Cookie: session=your-session-cookie"
   ```

## Notification Flow

1. **Deal Found**: When travel agent finds a matching deal
2. **Score Check**: Only deals with 70%+ match score trigger notifications
3. **Channel Selection**: 
   - Email sent if user has email
   - WhatsApp sent if user has WhatsApp number
4. **Mark as Sent**: Deal marked to prevent duplicate notifications

## Troubleshooting

### Email Not Sending
- Check SendGrid/SMTP credentials in Railway
- Verify sender email is authenticated
- Check spam folder
- Review Railway logs for errors

### WhatsApp Not Sending
- Ensure user joined Twilio sandbox (for testing)
- Verify phone number format includes country code
- Check Twilio account has credits
- Ensure number starts with 'whatsapp:' prefix

## Cost Considerations

### Email
- **SendGrid Free**: 100 emails/day
- **SendGrid Essentials**: $19.95/month for 50k emails
- **SMTP (Gmail)**: Free but limited to 500/day

### WhatsApp
- **Twilio Sandbox**: Free for testing
- **Twilio Production**: ~$0.005 per message
- **WhatsApp Business API**: Monthly fee + per message cost

## Privacy & GDPR

- Users must opt-in to notifications
- WhatsApp numbers stored securely
- Users can disable notifications in preferences
- All data encrypted in transit
- Comply with WhatsApp Business Policy

## Next Steps

1. Choose email provider (SendGrid recommended)
2. Set up Twilio for WhatsApp (start with sandbox)
3. Add environment variables to Railway
4. Test with your own account
5. Monitor notification delivery in logs