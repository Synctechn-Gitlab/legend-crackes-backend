def test_admin_login_success(client):
    response = client.post("/api/auth/login", json={
        "username": "testadmin",
        "password": "testpass123"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["user"]["username"] == "testadmin"


def test_admin_login_invalid_password(client):
    response = client.post("/api/auth/login", json={
        "username": "testadmin",
        "password": "wrongpassword"
    })
    assert response.status_code == 401
    assert "Invalid username/email or password" in response.json()["message"]


def test_admin_me_endpoint(client, admin_headers):
    response = client.get("/api/auth/me", headers=admin_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testadmin"
    assert data["email"] == "testadmin@sivakasi.com"


def test_admin_unauthorized_access(client):
    response = client.get("/api/auth/me")
    assert response.status_code == 401
