# URGENT: Railway Deployment Instructions

## 1. FIRST - Run Migration in Railway Console

After deployment, you MUST run this command in Railway console:

```bash
python migrations/ensure_admin_user.py
```

This creates the admin user in the database. Without this, authentication won't work.

## 2. Environment Variables

Ensure these are set in Railway:
- ADMIN_USERNAME=admin
- ADMIN_PASSWORD=changeme123!
- FLASK_SECRET_KEY=(generate random key)

## 3. Test the Fix

After running migration:
1. Login with admin/changeme123!
2. Go to /test
3. Should see "✅ User Found: admin (ID: X)"

## 4. School Holiday Data Issue

The current school holiday data is manually created. We need to implement:
- Gov.uk API integration for official school term dates
- Council website scraping for local variations
- Automatic updates for current year

This is a separate issue from the authentication problem.