#!/bin/bash
# drift_check.sh - Compare actual machine state vs INFRASTRUCTURE.md
# Part of Zero-Drift Infrastructure guardrails
# Run after any infrastructure changes

set -e

WORKSPACE="/root/jarvis-workspace"
EVIDENCE_DIR="$WORKSPACE/evidence"
TIMESTAMP=$(date +%Y-%m-%d_%H%M%S)
REPORT="$EVIDENCE_DIR/drift_check_$TIMESTAMP.md"

echo "# Drift Check Report" > "$REPORT"
echo "**Timestamp:** $(date -Iseconds)" >> "$REPORT"
echo "**Hostname:** $(hostname)" >> "$REPORT"
echo "" >> "$REPORT"

DRIFT_FOUND=0

# Function to check and report
check() {
    local name="$1"
    local expected="$2"
    local actual="$3"
    
    if [ "$expected" = "$actual" ]; then
        echo "✅ $name: OK" | tee -a "$REPORT"
    else
        echo "❌ $name: DRIFT DETECTED" | tee -a "$REPORT"
        echo "   Expected: $expected" | tee -a "$REPORT"
        echo "   Actual:   $actual" | tee -a "$REPORT"
        DRIFT_FOUND=1
    fi
}

echo "## System Checks" >> "$REPORT"
echo "" >> "$REPORT"

# Check hostname
EXPECTED_HOSTNAME="srv1078052"  # Update per machine
ACTUAL_HOSTNAME=$(hostname)
check "Hostname" "$EXPECTED_HOSTNAME" "$ACTUAL_HOSTNAME"

# Check Clawdbot service
EXPECTED_CLAWDBOT="active"
ACTUAL_CLAWDBOT=$(systemctl is-active clawdbot 2>/dev/null || echo "inactive")
check "Clawdbot Service" "$EXPECTED_CLAWDBOT" "$ACTUAL_CLAWDBOT"

# Check Docker containers (count)
EXPECTED_CONTAINERS=7
ACTUAL_CONTAINERS=$(docker ps -q 2>/dev/null | wc -l)
check "Docker Containers" "$EXPECTED_CONTAINERS" "$ACTUAL_CONTAINERS"

# Check Tailscale
EXPECTED_TAILSCALE="running"
ACTUAL_TAILSCALE=$(systemctl is-active tailscaled 2>/dev/null || echo "not running")
check "Tailscale" "active" "$ACTUAL_TAILSCALE"

# Check Git status
echo "" >> "$REPORT"
echo "## Git Status" >> "$REPORT"
echo "" >> "$REPORT"
cd "$WORKSPACE"
GIT_STATUS=$(git status --porcelain 2>/dev/null | wc -l)
if [ "$GIT_STATUS" -eq 0 ]; then
    echo "✅ Git: Clean (no uncommitted changes)" | tee -a "$REPORT"
else
    echo "⚠️ Git: $GIT_STATUS uncommitted changes" | tee -a "$REPORT"
    echo '```' >> "$REPORT"
    git status --short >> "$REPORT"
    echo '```' >> "$REPORT"
fi

# Check disk usage
echo "" >> "$REPORT"
echo "## Disk Usage" >> "$REPORT"
echo "" >> "$REPORT"
DISK_PERCENT=$(df / | tail -1 | awk '{print $5}' | tr -d '%')
if [ "$DISK_PERCENT" -gt 90 ]; then
    echo "🔴 Disk: ${DISK_PERCENT}% (CRITICAL)" | tee -a "$REPORT"
elif [ "$DISK_PERCENT" -gt 80 ]; then
    echo "🟡 Disk: ${DISK_PERCENT}% (WARNING)" | tee -a "$REPORT"
else
    echo "✅ Disk: ${DISK_PERCENT}% (OK)" | tee -a "$REPORT"
fi

# Summary
echo "" >> "$REPORT"
echo "## Summary" >> "$REPORT"
echo "" >> "$REPORT"
if [ "$DRIFT_FOUND" -eq 0 ]; then
    echo "✅ **No drift detected.** Machine state matches expected configuration." | tee -a "$REPORT"
else
    echo "❌ **DRIFT DETECTED.** Review above and either:" | tee -a "$REPORT"
    echo "1. Fix the machine to match INFRASTRUCTURE.md, OR" >> "$REPORT"
    echo "2. Update INFRASTRUCTURE.md to reflect intentional changes" >> "$REPORT"
fi

echo ""
echo "Report saved to: $REPORT"
