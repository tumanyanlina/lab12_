import pytest


def test_register_success(client):
    response = client.post("/auth/register", json={
        "email": "newuser@example.com",
        "username": "newuser",
        "password": "password123"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert data["username"] == "newuser"
    assert data["balance"] == 100000.0
    assert "id" in data


def test_register_duplicate_email(client, test_user):
    response = client.post("/auth/register", json={
        "email": "test@example.com",
        "username": "anotheruser",
        "password": "password123"
    })
    assert response.status_code == 400
    assert "Email already registered" in response.text


def test_register_duplicate_username(client, test_user):
    response = client.post("/auth/register", json={
        "email": "another@example.com",
        "username": "testuser",
        "password": "password123"
    })
    assert response.status_code == 400
    assert "Username already taken" in response.text


def test_register_invalid_email(client):
    response = client.post("/auth/register", json={
        "email": "invalid-email",
        "username": "user",
        "password": "password123"
    })
    assert response.status_code == 422


def test_register_short_password(client):
    response = client.post("/auth/register", json={
        "email": "user@example.com",
        "username": "user",
        "password": "123"
    })
    assert response.status_code == 422


def test_login_success(client, test_user):
    response = client.post("/auth/login", json={
        "username": "testuser",
        "password": "testpass123"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client, test_user):
    response = client.post("/auth/login", json={
        "username": "testuser",
        "password": "wrongpassword"
    })
    assert response.status_code == 401
    assert "Incorrect username or password" in response.text


def test_login_nonexistent_user(client):
    response = client.post("/auth/login", json={
        "username": "nonexistent",
        "password": "password"
    })
    assert response.status_code == 401