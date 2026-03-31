from fastapi.testclient import TestClient
from main import app
import time

client = TestClient(app)

def test_full_auth_flow():
    print("\n--- STARTING FULL AUTH FLOW TEST ---")

    # 1. Registration
    username = f"user_{int(time.time())}"
    password = "testpassword123"
    print(f"Testing Registration for: {username}...")
    response = client.post("/register", json={"username": username, "password": password})
    assert response.status_code == 200
    print("✅ Registration Successful")

    # 2. Login
    print("Testing Login...")
    response = client.post("/login", data={"username": username, "password": password})
    assert response.status_code == 200
    tokens = response.json()
    assert "access_token" in tokens
    assert "refresh_token" in tokens
    access_token = tokens["access_token"]
    refresh_token = tokens["refresh_token"]
    print("✅ Login Successful (Got Access & Refresh tokens)")

    # 3. Access Protected Route (Chat)
    print("Testing Protected Chat Route...")
    response = client.post(
        "/chat", 
        json={"message": "Hello, bot!"},
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    print(f"✅ Chat Access Successful. Bot said: {data['response'][:50]}...")

    # 4. Access Protected Route without token (Should fail)
    print("Testing Protected Route without token...")
    response = client.post("/chat", json={"message": "Fail me"})
    assert response.status_code == 401
    print("✅ Unauthenticated Access Blocked (Correct)")

    # 5. Refresh Token
    print("Testing Token Refresh...")
    response = client.post(f"/refresh?token={refresh_token}")
    assert response.status_code == 200
    new_tokens = response.json()
    assert "access_token" in new_tokens
    new_access_token = new_tokens["access_token"]
    print("✅ Token Refresh Successful (Got new Access token)")

    # 6. Access Protected Route with NEW token
    print("Testing Protected Route with NEW token...")
    response = client.post(
        "/chat", 
        json={"message": "Hello again!"},
        headers={"Authorization": f"Bearer {new_access_token}"}
    )
    assert response.status_code == 200
    print("✅ New Access Token Works")

    print("\n🚀 ALL AUTH TESTS PASSED!")

if __name__ == "__main__":
    try:
        test_full_auth_flow()
    except Exception as e:
        print(f"❌ TEST FAILED: {str(e)}")
