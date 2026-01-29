#!/usr/bin/env python3
"""
FactoryLM Signup API Test Script
Tests all endpoints and functionality
"""
import requests
import json
import time
from typing import Dict, Any

# Configuration
API_BASE = "http://127.0.0.1:8090"
ADMIN_API_KEY = "factorylm-admin-2026"

def test_endpoint(method: str, endpoint: str, data: Dict[Any, Any] = None, headers: Dict[str, str] = None) -> Dict[Any, Any]:
    """Test an API endpoint and return the response."""
    url = f"{API_BASE}{endpoint}"
    
    try:
        if method == "GET":
            response = requests.get(url, headers=headers, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=data, headers=headers, timeout=10)
        else:
            raise ValueError(f"Unsupported method: {method}")
        
        print(f"✅ {method} {endpoint} - Status: {response.status_code}")
        
        if response.headers.get('content-type', '').startswith('application/json'):
            return response.json()
        else:
            return {"raw_content": response.text}
            
    except Exception as e:
        print(f"❌ {method} {endpoint} - Error: {e}")
        return {"error": str(e)}

def run_tests():
    """Run comprehensive API tests."""
    print("🏭 FactoryLM Signup API Tests")
    print("=" * 50)
    
    # Test 1: Health check
    print("\n1. Testing health check...")
    health = test_endpoint("GET", "/health")
    
    # Test 2: Root endpoint
    print("\n2. Testing root endpoint...")
    root = test_endpoint("GET", "/")
    
    # Test 3: Public stats (should work even with no data)
    print("\n3. Testing public stats...")
    stats = test_endpoint("GET", "/api/stats")
    print(f"   Current signups: {stats.get('total_signups', 'N/A')}")
    
    # Test 4: Admin signups list (should require API key)
    print("\n4. Testing admin signups without API key (should fail)...")
    test_endpoint("GET", "/api/signups")
    
    print("\n5. Testing admin signups with API key...")
    admin_headers = {"X-API-Key": ADMIN_API_KEY}
    signups = test_endpoint("GET", "/api/signups", headers=admin_headers)
    print(f"   Current signups count: {len(signups) if isinstance(signups, list) else 'N/A'}")
    
    # Test 6: Valid signup
    print("\n6. Testing valid signup...")
    test_signup = {
        "name": "Test User",
        "email": f"test+{int(time.time())}@example.com",  # Unique email
        "company": "Test Company",
        "role": "Tester"
    }
    signup_result = test_endpoint("POST", "/api/signup", data=test_signup)
    print(f"   Result: {signup_result.get('message', 'N/A')}")
    
    # Test 7: Duplicate email (should fail gracefully)
    print("\n7. Testing duplicate email...")
    duplicate_result = test_endpoint("POST", "/api/signup", data=test_signup)
    print(f"   Result: {duplicate_result.get('message', 'N/A')}")
    
    # Test 8: Invalid email format
    print("\n8. Testing invalid email format...")
    invalid_signup = {
        "name": "Invalid User",
        "email": "not-an-email",
        "company": "Test Company", 
        "role": "Tester"
    }
    invalid_result = test_endpoint("POST", "/api/signup", data=invalid_signup)
    
    # Test 9: Missing required fields
    print("\n9. Testing missing required fields...")
    incomplete_signup = {
        "name": "Incomplete User",
        "email": "incomplete@example.com"
        # Missing company and role
    }
    incomplete_result = test_endpoint("POST", "/api/signup", data=incomplete_signup)
    
    # Test 10: Check updated stats
    print("\n10. Testing updated stats...")
    final_stats = test_endpoint("GET", "/api/stats")
    print(f"    Final signups: {final_stats.get('total_signups', 'N/A')}")
    
    print("\n" + "=" * 50)
    print("🎉 API tests completed!")
    print("\nTo monitor the service:")
    print("  sudo systemctl status factorylm-api")
    print("  sudo journalctl -u factorylm-api -f")
    print("\nAPI Documentation:")
    print(f"  {API_BASE}/docs")

if __name__ == "__main__":
    run_tests()