#!/bin/bash

# Railway deployment script for Travel AiGent
echo "🚀 Deploying Travel AiGent to Railway..."

# Set required environment variables
echo "📝 Setting environment variables..."

# Generated secure values
export FLASK_SECRET_KEY="3b70f247f83994f8916464c6cb4bdb0c318d4dc2bcf64a65a443254778160748"
export PASSWORD_SALT="7b9471e7e7fafa8b4b8d50ad10153721"
export ADMIN_USERNAME="admin"
export ADMIN_PASSWORD="changeme123!"
export FLASK_ENV="production"

# Database URL will be provided by Railway PostgreSQL service
echo "DATABASE_URL will be automatically set by Railway PostgreSQL service"

echo "✅ Environment variables configured"
echo "🔗 Railway project: https://railway.com/project/73c103df-45d7-40c0-82ad-c55a65b2a348"
echo ""
echo "🔧 Manual steps needed:"
echo "1. Go to Railway dashboard: https://railway.com/project/73c103df-45d7-40c0-82ad-c55a65b2a348"
echo "2. Click 'Deploy from GitHub repo'"
echo "3. Connect your GitHub repository: https://github.com/j99lef/Phoenix_Claude"
echo "4. Add the following environment variables in Railway settings:"
echo "   FLASK_SECRET_KEY=$FLASK_SECRET_KEY"
echo "   PASSWORD_SALT=$PASSWORD_SALT"
echo "   ADMIN_USERNAME=$ADMIN_USERNAME"
echo "   ADMIN_PASSWORD=$ADMIN_PASSWORD"
echo "   FLASK_ENV=production"
echo ""
echo "5. Railway will automatically detect railway.json and deploy"
echo "6. The app will be available at your Railway-provided URL"
echo ""
echo "🔐 Login credentials:"
echo "   Username: admin"
echo "   Password: changeme123!"
echo "   ⚠️  Change these immediately after first login!"