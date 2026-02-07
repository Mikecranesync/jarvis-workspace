#!/bin/bash
# Scrub .env files and add to Doppler
# Usage: ./env-to-doppler.sh [project] [config]

PROJECT="${1:-factorylm}"
CONFIG="${2:-dev}"

echo "🔍 Scanning for .env files..."

# Find all .env files
ENV_FILES=$(find . -name "*.env" -o -name ".env*" 2>/dev/null | grep -v node_modules | grep -v venv | grep -v __pycache__)

echo "Found:"
echo "$ENV_FILES"
echo ""

# Parse and collect unique keys
declare -A SECRETS

for file in $ENV_FILES; do
    echo "📄 Processing: $file"
    while IFS='=' read -r key value; do
        # Skip comments and empty lines
        [[ "$key" =~ ^#.*$ ]] && continue
        [[ -z "$key" ]] && continue
        # Remove quotes from value
        value="${value%\"}"
        value="${value#\"}"
        value="${value%\'}"
        value="${value#\'}"
        if [[ -n "$key" && -n "$value" ]]; then
            SECRETS["$key"]="$value"
            echo "  ✓ $key"
        fi
    done < "$file"
done

echo ""
echo "📦 Uploading ${#SECRETS[@]} secrets to Doppler ($PROJECT/$CONFIG)..."

# Upload to Doppler
for key in "${!SECRETS[@]}"; do
    doppler secrets set "$key=${SECRETS[$key]}" --project "$PROJECT" --config "$CONFIG" 2>/dev/null
done

echo "✅ Done! Run 'doppler secrets' to verify."
