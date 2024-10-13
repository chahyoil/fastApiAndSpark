# import pytest
# from fastapi import status

# def test_login(client):
#     response = client.post("/api/auth/token", data={"username": "testuser", "password": "testpassword"})
#     assert response.status_code == 200
#     assert "access_token" in response.json()

# def test_protected_route(client):
#     login_response = client.post("/api/auth/token", data={"username": "testuser", "password": "testpassword"})
#     assert login_response.status_code == 200, f"Login failed: {login_response.content}"
#     token = login_response.json()["access_token"]

#     headers = {"Authorization": f"Bearer {token}"}
#     response = client.get("/api/admin/protected", headers=headers)
#     print(f"Debug: Protected route response status: {response.status_code}")
#     print(f"Debug: Protected route response content: {response.content}")
#     assert response.status_code == 200, f"Expected 200, got {response.status_code}"

# def test_admin_route(client):
#     # Test with regular user
#     login_response = client.post("/api/auth/token", data={"username": "testuser", "password": "testpassword"})
#     assert login_response.status_code == 200, f"Regular user login failed: {login_response.content}"
#     token = login_response.json()["access_token"]
#     print(f"Debug: Regular user token: {token}")

#     headers = {"Authorization": f"Bearer {token}"}
#     response = client.get("/api/admin/admin-only-endpoint", headers=headers)
#     print(f"Debug: Regular user response status: {response.status_code}")
#     print(f"Debug: Regular user response content: {response.content}")

#     assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN], f"Expected 401 or 403, got {response.status_code}"

#     # Test with admin user
#     admin_login_response = client.post("/api/auth/token", data={"username": "adminuser", "password": "adminpassword"})
#     print(f"Debug: Admin login response status: {admin_login_response.status_code}")
#     print(f"Debug: Admin login response content: {admin_login_response.content}")

#     assert admin_login_response.status_code == 200, f"Admin login failed: {admin_login_response.content}"
    
#     admin_token = admin_login_response.json()["access_token"]
#     admin_headers = {"Authorization": f"Bearer {admin_token}"}
#     admin_response = client.get("/api/admin/admin-only-endpoint", headers=admin_headers)
#     print(f"Debug: Admin response status: {admin_response.status_code}")
#     print(f"Debug: Admin response content: {admin_response.content}")
#     assert admin_response.status_code == 200, f"Expected 200 for admin, got {admin_response.status_code}"
