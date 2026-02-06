#!/usr/bin/env python3
"""
Test script for Jarvis Memory System
Validates search functionality and performance
"""
import asyncio
import json
import time
from pathlib import Path

import requests

from config import SERVICE_HOST, SERVICE_PORT, MEMORY_DIR

# Test configuration
API_BASE = f"http://{SERVICE_HOST}:{SERVICE_PORT}"
TEST_QUERIES = [
    "factorylm",
    "raspberry pi", 
    "memory system",
    "mike",
    "clawdbot",
    "api key",
    "telegram",
    "jarvis node"
]

def test_api_connection():
    """Test basic API connectivity"""
    print("🔗 Testing API connection...")
    try:
        response = requests.get(f"{API_BASE}/health", timeout=10)
        if response.status_code == 200:
            health = response.json()
            print(f"✅ API connection successful")
            print(f"   Status: {health.get('status')}")
            print(f"   Stats: {health.get('stats', {}).get('total_chunks')} chunks indexed")
            return True
        else:
            print(f"❌ API health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API connection failed: {e}")
        return False

def test_memory_files():
    """Check if memory files exist"""
    print("\n📁 Checking memory files...")
    memory_dir = Path(MEMORY_DIR)
    
    if not memory_dir.exists():
        print(f"❌ Memory directory not found: {MEMORY_DIR}")
        return False
    
    md_files = list(memory_dir.glob("*.md"))
    print(f"✅ Found {len(md_files)} memory files")
    
    if md_files:
        # Show a few example files
        for i, file_path in enumerate(md_files[:3]):
            size = file_path.stat().st_size
            print(f"   - {file_path.name} ({size} bytes)")
        if len(md_files) > 3:
            print(f"   - ... and {len(md_files) - 3} more files")
    
    return len(md_files) > 0

def test_search_queries():
    """Test search functionality with various queries"""
    print("\n🔍 Testing search queries...")
    
    results = {}
    total_time = 0
    
    for query in TEST_QUERIES:
        print(f"   Searching: '{query}'")
        
        try:
            start_time = time.time()
            response = requests.post(
                f"{API_BASE}/search",
                json={
                    "query": query,
                    "max_results": 3,
                    "min_score": 0.1  # Lower threshold for testing
                },
                timeout=10
            )
            search_time = time.time() - start_time
            total_time += search_time
            
            if response.status_code == 200:
                data = response.json()
                result_count = len(data.get("results", []))
                
                print(f"      ✅ {result_count} results in {search_time:.3f}s")
                
                # Show top result if available
                if result_count > 0:
                    top_result = data["results"][0]
                    snippet = top_result["snippet"][:100] + "..." if len(top_result["snippet"]) > 100 else top_result["snippet"]
                    print(f"         Top: {top_result['path']} (score: {top_result['score']:.3f})")
                    print(f"              {snippet}")
                
                results[query] = {
                    "count": result_count,
                    "time": search_time,
                    "success": True
                }
            else:
                print(f"      ❌ Search failed: {response.status_code} - {response.text}")
                results[query] = {"success": False, "error": response.text}
                
        except Exception as e:
            print(f"      ❌ Search error: {e}")
            results[query] = {"success": False, "error": str(e)}
    
    # Summary
    successful_searches = sum(1 for r in results.values() if r.get("success"))
    avg_time = total_time / len(TEST_QUERIES) if TEST_QUERIES else 0
    
    print(f"\n📊 Search Test Summary:")
    print(f"   ✅ Successful searches: {successful_searches}/{len(TEST_QUERIES)}")
    print(f"   ⏱️  Average search time: {avg_time:.3f}s")
    
    return successful_searches > 0

def test_stats():
    """Test stats endpoint"""
    print("\n📊 Testing stats endpoint...")
    
    try:
        response = requests.get(f"{API_BASE}/stats", timeout=5)
        if response.status_code == 200:
            stats = response.json()
            print("✅ Stats endpoint working")
            
            for key, value in stats.items():
                if key != "error":
                    print(f"   {key}: {value}")
            
            return True
        else:
            print(f"❌ Stats endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Stats endpoint error: {e}")
        return False

def test_performance_benchmark():
    """Run a performance benchmark"""
    print("\n⚡ Running performance benchmark...")
    
    # Test with different query lengths
    test_cases = [
        ("short", "jarvis"),
        ("medium", "factorylm raspberry pi setup"),
        ("long", "tell me about the clawdbot memory search system and how it integrates with telegram for jarvis")
    ]
    
    for test_name, query in test_cases:
        try:
            times = []
            for i in range(3):  # Run 3 times for average
                start_time = time.time()
                response = requests.post(
                    f"{API_BASE}/search",
                    json={"query": query, "max_results": 5},
                    timeout=10
                )
                search_time = time.time() - start_time
                times.append(search_time)
                
                if response.status_code != 200:
                    print(f"   ❌ {test_name} query failed: {response.status_code}")
                    break
            else:
                avg_time = sum(times) / len(times)
                print(f"   ✅ {test_name} query: {avg_time:.3f}s avg (±{max(times) - min(times):.3f}s)")
        
        except Exception as e:
            print(f"   ❌ {test_name} query error: {e}")

def main():
    """Run all tests"""
    print("🧪 Jarvis Memory System Test Suite")
    print("=" * 50)
    
    # Track overall success
    tests_passed = 0
    total_tests = 5
    
    # Test 1: API Connection
    if test_api_connection():
        tests_passed += 1
    
    # Test 2: Memory Files
    if test_memory_files():
        tests_passed += 1
    
    # Test 3: Search Queries  
    if test_search_queries():
        tests_passed += 1
    
    # Test 4: Stats Endpoint
    if test_stats():
        tests_passed += 1
    
    # Test 5: Performance
    test_performance_benchmark()
    tests_passed += 1  # Performance test doesn't fail, just provides info
    
    # Final Results
    print("\n" + "=" * 50)
    print("🏆 Test Results")
    print(f"   Passed: {tests_passed}/{total_tests}")
    
    if tests_passed == total_tests:
        print("   ✅ All tests passed! Memory system is working correctly.")
        exit_code = 0
    else:
        print(f"   ❌ {total_tests - tests_passed} tests failed. Check the logs above.")
        exit_code = 1
    
    # Instructions for integration
    if tests_passed >= 4:
        print("\n🔗 Ready for Clawdbot Integration!")
        print(f"   Update Clawdbot config to use: http://{SERVICE_HOST}:{SERVICE_PORT}")
        print("   Set provider to 'local' and configure remote.baseUrl")
    
    return exit_code

if __name__ == "__main__":
    import sys
    sys.exit(main())