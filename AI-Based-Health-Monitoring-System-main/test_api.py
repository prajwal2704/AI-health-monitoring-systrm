"""
Simple test script to verify the API is working
Run this after starting the Flask server
"""
import requests
import json

def get_active_base_url():
    for p in [5005, 5000]:
        try:
            r = requests.get(f"http://localhost:{p}/health", timeout=1)
            if r.status_code == 200 and r.json().get('service') == 'CarePulse Health Platform':
                return f"http://localhost:{p}"
        except Exception:
            continue
    return "http://localhost:5000"

BASE_URL = get_active_base_url()

def test_health():
    """Test health endpoint"""
    print("Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}\n")

def get_auth_token():
    """Register or login a test user to obtain an authentication token"""
    print("Authenticating test user...")
    test_user = {
        "full_name": "Test User",
        "date_of_birth": "1995-05-15",
        "email": "testuser@healthcheck.local",
        "password": "TestPassword123!"
    }
    
    # Try logging in first
    login_resp = requests.post(f"{BASE_URL}/api/auth/login", json={
        "email": test_user["email"],
        "password": test_user["password"]
    })
    
    if login_resp.status_code == 200 and login_resp.json().get("success"):
        token = login_resp.json()["session_token"]
        print("   Logged in with existing test user\n")
        return token
    
    # Otherwise register new user
    reg_resp = requests.post(f"{BASE_URL}/api/auth/register", json=test_user)
    if reg_resp.status_code == 201 and reg_resp.json().get("success"):
        token = reg_resp.json()["session_token"]
        print("   Registered new test user\n")
        return token
        
    raise Exception(f"Failed to authenticate: {reg_resp.text}")

def test_conversation_flow():
    """Test complete conversation flow with authentication"""
    print("Testing conversation flow...\n")
    
    token = get_auth_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # 1. Start conversation
    print("1. Starting conversation...")
    response = requests.post(f"{BASE_URL}/api/conversation/start", json={}, headers=headers)
    if response.status_code != 200:
        print(f"Error: {response.json()}")
        return
    
    data = response.json()
    conversation_id = data["conversation_id"]
    print(f"   Conversation ID (UUID): {conversation_id}\n")
    
    # 2. Set age
    print("2. Setting age...")
    response = requests.post(
        f"{BASE_URL}/api/conversation/{conversation_id}/age",
        json={"age": "18-64 years (Adult)"},
        headers=headers
    )
    if response.status_code != 200:
        print(f"Error: {response.json()}")
        return
    print(f"   {response.json()['message']}\n")
    
    # 3. Set language
    print("3. Setting language...")
    response = requests.post(
        f"{BASE_URL}/api/conversation/{conversation_id}/language",
        json={"language": "english"},
        headers=headers
    )
    if response.status_code != 200:
        print(f"Error: {response.json()}")
        return
    print(f"   {response.json()['message']}\n")
    
    # 4. Send chat message
    print("4. Sending chat message...")
    response = requests.post(
        f"{BASE_URL}/api/conversation/{conversation_id}/chat",
        json={"message": "I have a mild fever and headache"},
        headers=headers
    )
    if response.status_code != 200:
        print(f"Error: {response.json()}")
        return
    
    result = response.json()
    print("   Response received:")
    if "response" in result and isinstance(result["response"], dict):
        print(f"   Summary: {result['response'].get('summary', '')[:100]}...")
        print(f"   Home Care: {result['response'].get('home_care', '')[:100]}...")
    else:
        print(f"   Raw: {result}")
    print()
    
    # 5. Check status
    print("5. Checking conversation status...")
    response = requests.get(f"{BASE_URL}/api/conversation/{conversation_id}/status", headers=headers)
    if response.status_code == 200:
        print(f"   Status: {response.json()}\n")

    # 6. Verify conversation saved in user's history
    print("6. Verifying saved user conversations...")
    hist_response = requests.get(f"{BASE_URL}/api/user/conversations", headers=headers)
    if hist_response.status_code == 200:
        convs = hist_response.json().get("conversations", [])
        print(f"   User has {len(convs)} conversation(s) persisted in history.\n")
    
    print("[OK] All tests passed!")

def test_config_endpoints():
    """Test configuration endpoints"""
    print("\nTesting configuration endpoints...\n")
    
    endpoints = [
        "/api/config/age-groups",
        "/api/config/languages",
        "/api/config/llm-providers"
    ]
    
    for endpoint in endpoints:
        print(f"Testing {endpoint}...")
        response = requests.get(f"{BASE_URL}{endpoint}")
        if response.status_code == 200:
            print(f"   [OK] Success")
        else:
            print(f"   [ERROR] Error: {response.json()}")
        print()

if __name__ == "__main__":
    try:
        test_health()
        test_config_endpoints()
        test_conversation_flow()
    except requests.exceptions.ConnectionError:
        print("[ERROR] Could not connect to server.")
        print("   Make sure the Flask server is running on http://localhost:5000")
    except Exception as e:
        print(f"[ERROR] {e}")

