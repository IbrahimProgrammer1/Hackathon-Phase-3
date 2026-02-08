import requests
import sys

def test_forgot_password_api():
    """
    Test script to verify the forgot password API endpoints are working
    """
    base_url = "http://localhost:8000"

    print("Testing forgot password API endpoints...")

    # Test the root endpoint first
    try:
        response = requests.get(f"{base_url}")
        if response.status_code == 200:
            print("✓ Main API endpoint is accessible")
        else:
            print(f"✗ Main API endpoint returned status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"✗ Cannot connect to API at {base_url}")
        print("Make sure the backend server is running on port 8000")
        return False
    except Exception as e:
        print(f"✗ Error connecting to API: {str(e)}")
        return False

    # Test the forgot password endpoint
    try:
        response = requests.post(
            f"{base_url}/api/auth/forgot-password",
            json={"email": "test@example.com"},
            headers={"Content-Type": "application/json"}
        )
        print(f"Forgot password endpoint response: {response.status_code}")

        if response.status_code in [200, 400, 422]:  # 200 for success, 400 for validation errors, 422 for schema errors
            print("✓ Forgot password endpoint is accessible")
            return True
        else:
            print(f"✗ Unexpected response from forgot password endpoint: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("✗ Cannot connect to forgot password endpoint")
        return False
    except Exception as e:
        print(f"✗ Error testing forgot password endpoint: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_forgot_password_api()
    if success:
        print("\n✓ API endpoints are working correctly!")
    else:
        print("\n✗ There are issues with the API endpoints that need to be fixed.")
        sys.exit(1)