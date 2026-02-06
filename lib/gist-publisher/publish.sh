#!/bin/bash
# Gist Publisher - Publish any document to GitHub Gist
# Usage: ./publish.sh <filepath> [description] [--private]

set -e

FILEPATH="$1"
DESCRIPTION="${2:-Auto-published document}"
VISIBILITY="--public"

if [[ "$3" == "--private" ]]; then
    VISIBILITY=""
fi

if [[ -z "$FILEPATH" ]]; then
    echo "Usage: ./publish.sh <filepath> [description] [--private]"
    exit 1
fi

if [[ ! -f "$FILEPATH" ]]; then
    echo "Error: File not found: $FILEPATH"
    exit 1
fi

# Publish to Gist
GIST_URL=$(gh gist create "$FILEPATH" $VISIBILITY --desc "$DESCRIPTION" 2>&1 | grep "https://gist.github.com")

if [[ -z "$GIST_URL" ]]; then
    echo "Error: Failed to create Gist"
    exit 1
fi

# Cache the URL
CACHE_DIR=$(dirname "$FILEPATH")
CACHE_FILE="$CACHE_DIR/.gist_urls"
FILENAME=$(basename "$FILEPATH")

# Add or update cache entry
if [[ -f "$CACHE_FILE" ]]; then
    # Remove old entry for this file
    grep -v "^$FILENAME:" "$CACHE_FILE" > "$CACHE_FILE.tmp" 2>/dev/null || true
    mv "$CACHE_FILE.tmp" "$CACHE_FILE"
fi
echo "$FILENAME:$GIST_URL" >> "$CACHE_FILE"

echo "$GIST_URL"
