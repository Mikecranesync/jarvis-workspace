#!/usr/bin/env python3
"""
ShowUI Computer Use - Test Script
Tests remote visual computer control via Gradio API
"""

from gradio_client import Client
import time

SHOWUI_URL = "https://a5f0c2094e874e1cee.gradio.live"

def test_connection():
    """Test basic connection to ShowUI"""
    print("🔌 Testing connection...")
    try:
        client = Client(SHOWUI_URL)
        print("✅ Connected to ShowUI!")
        return client
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return None

def test_simple_command(client, command: str):
    """Send a simple command and get response"""
    print(f"\n🎮 Sending command: '{command}'")
    try:
        result = client.predict(
            user_input=command,
            api_name="/process_input"
        )
        print(f"📤 Response: {result}")
        return result
    except Exception as e:
        print(f"❌ Command failed: {e}")
        return None

def run_tests():
    """Run test suite"""
    print("=" * 50)
    print("ShowUI Computer Use - Test Suite")
    print("=" * 50)
    
    # Test 1: Connection
    client = test_connection()
    if not client:
        return False
    
    # Test 2: Simple query (should just describe, not act)
    test_simple_command(client, "What do you see on the screen?")
    
    # Wait a bit
    time.sleep(2)
    
    # Test 3: Simple action (careful - this will actually click!)
    # Uncomment to test actual control:
    # test_simple_command(client, "Move the mouse to the center of the screen")
    
    print("\n" + "=" * 50)
    print("✅ Tests complete!")
    print("=" * 50)
    return True

if __name__ == "__main__":
    run_tests()
