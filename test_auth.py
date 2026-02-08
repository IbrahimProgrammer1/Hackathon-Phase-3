import requests
import sys

BASE_URL = "http://localhost:8000/api"

def test_auth():
    print("Testing Authentication Flow...")
    
    # 1. Register
    print("\n1. Registering user...")
    register_data = {
        "name": "Test User",
        "email": "test_script@example.com",
        "password": "password123"
    }
    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
        if response.status_code == 200:
            print("   Success: User registered.")
            print(f"   Response: {response.json()}")
        elif response.status_code == 400 and "Email already registered" in response.text:
            print("   User already exists, proceeding to login.")
        else:
            print(f"   Failed: {response.status_code} - {response.text}")
            return
    except Exception as e:
        print(f"   Error: {e}")
        return

    # 2. Login
    print("\n2. Logging in...")
    login_data = {
        "email": "test_script@example.com",
        "password": "password123"
    }
    token = None
    user_id = None
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        if response.status_code == 200:
            data = response.json()
            token = data.get("token")
            user_id = data.get("user").get("id")
            print("   Success: Logged in.")
            print(f"   Token: {token[:20]}...")
            print(f"   User ID: {user_id}")
        else:
            print(f"   Failed: {response.status_code} - {response.text}")
            return
    except Exception as e:
        print(f"   Error: {e}")
        return

    # 3. Get Tasks
    print("\n3. Fetching tasks...")
    if not token or not user_id:
        print("   Cannot fetch tasks without token/user_id.")
        return

    headers = {
        "Authorization": f"Bearer {token}"
    }
    try:
        response = requests.get(f"{BASE_URL}/{user_id}/tasks", headers=headers)
        if response.status_code == 200:
            print("   Success: Tasks fetched.")
            print(f"   Tasks: {response.json()}")
        else:
            print(f"   Failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"   Error: {e}")

if __name__ == "__main__":
    test_auth()
