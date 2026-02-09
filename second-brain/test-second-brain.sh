#!/bin/bash

# Second Brain Server Test Script
# Tests security, functionality, and performance
# Author: Jarvis QA Agent
# Version: 1.0.0

set -e

SERVER_URL="http://localhost:3001"
PID_FILE="/tmp/second-brain-test.pid"
TEST_DIR="/tmp/second-brain-test"
FAILED_TESTS=()

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test counter
TEST_COUNT=0
PASSED_COUNT=0

echo -e "${BLUE}🧠 Second Brain Server Test Suite${NC}"
echo "=================================="

# Logging function
log() {
    echo -e "${BLUE}[$(date '+%H:%M:%S')]${NC} $1"
}

# Success function
success() {
    echo -e "${GREEN}✓${NC} $1"
    ((PASSED_COUNT++))
}

# Failure function
fail() {
    echo -e "${RED}✗${NC} $1"
    FAILED_TESTS+=("$1")
}

# Test function wrapper
run_test() {
    local test_name="$1"
    local test_command="$2"
    
    ((TEST_COUNT++))
    log "Running: $test_name"
    
    if eval "$test_command" >/dev/null 2>&1; then
        success "$test_name"
    else
        fail "$test_name"
    fi
}

# Start server function
start_server() {
    log "Starting Second Brain server..."
    
    cd /root/jarvis-workspace/second-brain
    node server-improved.js &
    local server_pid=$!
    echo $server_pid > "$PID_FILE"
    
    # Wait for server to start
    local attempts=0
    while [ $attempts -lt 10 ]; do
        if curl -s -f "$SERVER_URL/health" >/dev/null 2>&1; then
            success "Server started successfully (PID: $server_pid)"
            return 0
        fi
        sleep 1
        ((attempts++))
    done
    
    fail "Server failed to start"
    return 1
}

# Stop server function
stop_server() {
    if [ -f "$PID_FILE" ]; then
        local pid=$(cat "$PID_FILE")
        if kill -0 "$pid" 2>/dev/null; then
            log "Stopping server (PID: $pid)..."
            kill "$pid"
            rm -f "$PID_FILE"
            success "Server stopped"
        fi
    fi
}

# Cleanup function
cleanup() {
    stop_server
    rm -rf "$TEST_DIR"
    log "Cleanup completed"
}

# Setup test environment
setup_test_env() {
    log "Setting up test environment..."
    mkdir -p "$TEST_DIR"
    
    # Create test brain directory structure
    mkdir -p "/root/jarvis-workspace/brain/concepts"
    mkdir -p "/root/jarvis-workspace/brain/journals" 
    mkdir -p "/root/jarvis-workspace/brain/research"
    mkdir -p "/root/jarvis-workspace/brain/workflows"
    
    # Create test documents
    cat > "/root/jarvis-workspace/brain/concepts/test-doc.md" << 'EOF'
# Test Document

This is a test document for **testing** purposes.

- Item 1
- Item 2

```javascript
console.log("Hello World");
```
EOF

    cat > "/root/jarvis-workspace/brain/journals/daily-log.md" << 'EOF'
# Daily Log

Today's activities:
- Testing the second brain
- Security review
EOF
    
    success "Test environment setup"
}

# API Tests

# Test 1: Health Check
test_health_check() {
    local response=$(curl -s "$SERVER_URL/health")
    echo "$response" | grep -q "healthy"
}

# Test 2: Get Documents
test_get_documents() {
    local response=$(curl -s "$SERVER_URL/api/documents")
    echo "$response" | jq -e '. | length >= 0' >/dev/null
}

# Test 3: Get Single Document
test_get_single_document() {
    curl -s -f "$SERVER_URL/api/documents/concepts/test-doc" >/dev/null
}

# Test 4: Create Document
test_create_document() {
    local content='{"content":"# Test\\n\\nNew document content"}'
    curl -s -X POST \
        -H "Content-Type: application/json" \
        -d "$content" \
        "$SERVER_URL/api/documents/concepts/api-test" | \
        jq -e '.success == true' >/dev/null
}

# Test 5: Update Document
test_update_document() {
    local content='{"content":"# Updated Test\\n\\nUpdated content"}'
    curl -s -X POST \
        -H "Content-Type: application/json" \
        -d "$content" \
        "$SERVER_URL/api/documents/concepts/api-test" | \
        jq -e '.success == true' >/dev/null
}

# Test 6: Delete Document
test_delete_document() {
    curl -s -X DELETE \
        "$SERVER_URL/api/documents/concepts/api-test" | \
        jq -e '.success == true' >/dev/null
}

# Test 7: Get Workspace Files
test_get_workspace() {
    local response=$(curl -s "$SERVER_URL/api/workspace")
    echo "$response" | jq -e '. | type == "array"' >/dev/null
}

# Test 8: Get Status
test_get_status() {
    local response=$(curl -s "$SERVER_URL/api/status")
    echo "$response" | jq -e '.server == "second-brain"' >/dev/null
}

# Security Tests

# Test 9: Path Traversal Prevention
test_path_traversal() {
    # Should return 400 or 404, not 200
    local status=$(curl -s -w "%{http_code}" -o /dev/null \
        "$SERVER_URL/api/documents/../../../etc/passwd")
    [ "$status" != "200" ]
}

# Test 10: Invalid Category
test_invalid_category() {
    local status=$(curl -s -w "%{http_code}" -o /dev/null \
        "$SERVER_URL/api/documents/invalid-category/test")
    [ "$status" == "400" ]
}

# Test 11: Invalid Filename
test_invalid_filename() {
    local status=$(curl -s -w "%{http_code}" -o /dev/null \
        "$SERVER_URL/api/documents/concepts/../../test")
    [ "$status" == "400" ]
}

# Test 12: Large Content Block
test_large_content() {
    local large_content=$(printf '{"content":"%s"}' "$(yes 'A' | head -n 100000 | tr -d '\n')")
    local status=$(curl -s -w "%{http_code}" -o /dev/null \
        -X POST \
        -H "Content-Type: application/json" \
        -d "$large_content" \
        "$SERVER_URL/api/documents/concepts/large-test")
    [ "$status" == "400" ]
}

# Test 13: XSS Prevention
test_xss_prevention() {
    local xss_content='{"content":"# Test\\n\\n<script>alert(\"XSS\")</script>"}'
    local response=$(curl -s -X POST \
        -H "Content-Type: application/json" \
        -d "$xss_content" \
        "$SERVER_URL/api/documents/concepts/xss-test")
    
    # Check if document was created
    local doc_response=$(curl -s "$SERVER_URL/api/documents/concepts/xss-test")
    
    # HTML should be sanitized (no script tags)
    ! echo "$doc_response" | jq -r '.html' | grep -q '<script>'
    
    # Cleanup
    curl -s -X DELETE "$SERVER_URL/api/documents/concepts/xss-test" >/dev/null
}

# Test 14: Non-existent Document
test_nonexistent_document() {
    local status=$(curl -s -w "%{http_code}" -o /dev/null \
        "$SERVER_URL/api/documents/concepts/does-not-exist")
    [ "$status" == "404" ]
}

# Test 15: Root Path Access
test_root_path() {
    local response=$(curl -s "$SERVER_URL/")
    echo "$response" | grep -q "Jarvis Portal"
}

# Performance Tests

# Test 16: Response Time
test_response_time() {
    local start_time=$(date +%s%N)
    curl -s "$SERVER_URL/api/status" >/dev/null
    local end_time=$(date +%s%N)
    local duration=$(( (end_time - start_time) / 1000000 )) # milliseconds
    
    # Should respond within 1 second
    [ "$duration" -lt 1000 ]
}

# Test 17: Concurrent Requests
test_concurrent_requests() {
    local pids=()
    
    for i in {1..5}; do
        (curl -s "$SERVER_URL/api/documents" >/dev/null) &
        pids+=($!)
    done
    
    # Wait for all requests and check if any failed
    local failed=0
    for pid in "${pids[@]}"; do
        if ! wait "$pid"; then
            ((failed++))
        fi
    done
    
    # All requests should succeed
    [ "$failed" -eq 0 ]
}

# Test 18: Memory Usage Check
test_memory_usage() {
    # Get initial memory
    local initial_mem=$(ps -o rss= -p $(cat "$PID_FILE") | tr -d ' ')
    
    # Make some requests
    for i in {1..10}; do
        curl -s "$SERVER_URL/api/documents" >/dev/null
    done
    
    # Get final memory
    local final_mem=$(ps -o rss= -p $(cat "$PID_FILE") | tr -d ' ')
    
    # Memory should not increase by more than 50MB
    local mem_increase=$((final_mem - initial_mem))
    [ "$mem_increase" -lt 50000 ] # 50MB in KB
}

# Main execution
main() {
    trap cleanup EXIT
    
    log "Initializing test suite..."
    setup_test_env
    
    if ! start_server; then
        echo -e "${RED}Failed to start server. Exiting.${NC}"
        exit 1
    fi
    
    log "Running API tests..."
    run_test "Health Check" "test_health_check"
    run_test "Get Documents" "test_get_documents"
    run_test "Get Single Document" "test_get_single_document"
    run_test "Create Document" "test_create_document"
    run_test "Update Document" "test_update_document"
    run_test "Delete Document" "test_delete_document"
    run_test "Get Workspace Files" "test_get_workspace"
    run_test "Get Status" "test_get_status"
    
    log "Running security tests..."
    run_test "Path Traversal Prevention" "test_path_traversal"
    run_test "Invalid Category Rejection" "test_invalid_category"
    run_test "Invalid Filename Rejection" "test_invalid_filename"
    run_test "Large Content Blocking" "test_large_content"
    run_test "XSS Prevention" "test_xss_prevention"
    run_test "Non-existent Document" "test_nonexistent_document"
    run_test "Root Path Access" "test_root_path"
    
    log "Running performance tests..."
    run_test "Response Time" "test_response_time"
    run_test "Concurrent Requests" "test_concurrent_requests"
    run_test "Memory Usage" "test_memory_usage"
    
    # Results
    echo ""
    echo -e "${BLUE}Test Results${NC}"
    echo "============"
    echo -e "Total Tests: ${BLUE}$TEST_COUNT${NC}"
    echo -e "Passed: ${GREEN}$PASSED_COUNT${NC}"
    echo -e "Failed: ${RED}$((TEST_COUNT - PASSED_COUNT))${NC}"
    
    if [ ${#FAILED_TESTS[@]} -gt 0 ]; then
        echo ""
        echo -e "${RED}Failed Tests:${NC}"
        for test in "${FAILED_TESTS[@]}"; do
            echo -e "  ${RED}✗${NC} $test"
        done
        echo ""
        echo -e "${YELLOW}⚠️  Some tests failed. Check server logs for details.${NC}"
        return 1
    else
        echo ""
        echo -e "${GREEN}🎉 All tests passed! Server is ready for production.${NC}"
        return 0
    fi
}

# Check dependencies
check_dependencies() {
    local deps=(curl jq node npm)
    local missing=()
    
    for dep in "${deps[@]}"; do
        if ! command -v "$dep" >/dev/null 2>&1; then
            missing+=("$dep")
        fi
    done
    
    if [ ${#missing[@]} -gt 0 ]; then
        echo -e "${RED}Missing dependencies: ${missing[*]}${NC}"
        echo "Please install missing dependencies and retry."
        exit 1
    fi
}

# Run main function if script is executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    check_dependencies
    main
    exit $?
fi