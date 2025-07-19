# TravelAiGent Version Management

## Current Version: 1.2.0+build.12

This document outlines the version management strategy for TravelAiGent.

## Versioning Strategy

We follow Semantic Versioning (SemVer) with the format: `MAJOR.MINOR.PATCH+build.NUMBER`

- **MAJOR**: Breaking changes or significant architectural updates
- **MINOR**: New features or substantial improvements
- **PATCH**: Bug fixes and minor improvements
- **BUILD**: Incremental build number for each deployment

## Version Information

### Accessing Version Information

1. **In Application**:
   - Version is displayed in template footers
   - Available in health check endpoint: `/health`
   - Detailed version info at: `/api/version`

2. **In Code**:
   ```python
   from version import VERSION, VERSION_FULL, get_version_info
   ```

3. **API Response Example**:
   ```json
   {
     "version": "1.2.0",
     "version_full": "1.2.0+build.12",
     "build": 12,
     "build_date": "2025-01-19",
     "features": {
       "gmail_notifications": true,
       "password_reset": true,
       "whatsapp_notifications": false
     }
   }
   ```

## Version History

### v1.2.0 (2025-01-19) - Gmail Integration
- Replaced Twilio/SendGrid with Gmail SMTP for simplicity
- Implemented password reset functionality with secure tokens
- Added password_reset_tokens database table
- Removed WhatsApp notification dependencies
- Simplified email configuration to use Gmail app passwords

### v1.1.0 (2025-01-18) - Notifications & Fixes
- Added WhatsApp notifications via Twilio
- Implemented email notifications via SendGrid
- Fixed critical production issues
- Added deal search functionality
- Fixed authentication persistence

### v1.0.0 (2025-01-17) - Initial Release
- User registration and authentication
- Travel brief creation and management
- People profiles and travel groups
- Amadeus API integration for flight deals
- Basic deal matching algorithm

## Updating Version

When making changes:

1. **Update version.py**:
   - Increment VERSION_PATCH for bug fixes
   - Increment VERSION_MINOR for new features
   - Increment VERSION_MAJOR for breaking changes
   - Always increment BUILD_NUMBER

2. **Update VERSION_HISTORY** in version.py with changes

3. **Commit with version in message**:
   ```bash
   git commit -m "v1.2.0+build.12: Add Gmail notifications and password reset"
   ```

4. **Tag releases**:
   ```bash
   git tag -a v1.2.0 -m "Release version 1.2.0"
   git push origin v1.2.0
   ```

## Deployment Notes

- Version is automatically included in logs during startup
- Health endpoints return current version for monitoring
- Railway deployments should update build number
- Version is visible in application UI for support purposes

## Best Practices

1. **Always increment build number** for any deployment
2. **Document changes** in VERSION_HISTORY
3. **Include version in commit messages** for traceability
4. **Test version endpoints** after deployment
5. **Monitor version** in production logs

## Version Display Locations

- Login page (bottom right corner)
- Home page footer
- Health check endpoint: `/health`
- Version API endpoint: `/api/version`
- Application logs on startup
- Error reports and support tickets