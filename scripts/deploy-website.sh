#!/bin/bash
# Deploy FactoryLM website to production (Hostinger)
# Usage: ./deploy-website.sh

set -e

LANDING_PAGE="/root/jarvis-workspace/landing-page"
SSH_KEY="$HOME/.ssh/vps_deploy_key"
REMOTE="root@72.60.175.144"
WEB_ROOT="/var/www/factorylm"

echo "🚀 Deploying FactoryLM website..."

# Deploy main page
echo "   Copying index.html..."
scp -i "$SSH_KEY" "$LANDING_PAGE/index.html" "$REMOTE:$WEB_ROOT/"

# Deploy blog
echo "   Copying blog/..."
scp -i "$SSH_KEY" -r "$LANDING_PAGE/blog" "$REMOTE:$WEB_ROOT/"

# Verify
echo "   Verifying..."
LOGO=$(curl -s https://factorylm.com | grep 'class="logo"')
if [[ "$LOGO" == *'href="/"'* ]]; then
    echo "✅ Deployed successfully!"
else
    echo "⚠️  Deploy may have issues. Check manually."
fi
