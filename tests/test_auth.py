def test_user_can_register_and_login(client):
    res = client.post(
        "/auth/register",
        json={
            "email": "user@example.com",
            "password": "StrongPass123",
            "name": "Test",
            "surname": "User",
        },
    )
    print(res.get_json())
    assert res.status_code == 201

    res = client.post(
        "/auth/login", json={"email": "user@example.com", "password": "StrongPass123"}
    )
    print(res.get_json())
    assert res.status_code == 200
    assert "access_token" in res.get_json()


def test_register_with_existing_email(client):
    client.post(
        "/auth/register",
        json={
            "email": "user@example.com",
            "password": "Secure123",
            "name": "Test",
            "surname": "User",
        },
    )
    res = client.post(
        "/auth/register",
        json={
            "email": "user@example.com",
            "password": "Secure123",
            "name": "Another",
            "surname": "User",
        },
    )
    assert res.status_code == 400
    assert "User already exists" in res.get_data(as_text=True)


def test_login_with_invalid_credentials(client):
    res = client.post(
        "/auth/login", json={"email": "nonexistent@example.com", "password": "wrong"}
    )
    assert res.status_code == 401
    assert "Invalid credentials" in res.get_data(as_text=True)


def test_register_with_too_short_password(client):
    res = client.post(
        "/auth/register",
        json={
            "email": "short@example.com",
            "password": "abc1",  # < 8
            "name": "Short",
            "surname": "User",
        },
    )
    assert res.status_code == 400
    assert "at least 8 characters" in res.get_data(as_text=True)


def test_register_with_password_without_digits(client):
    res = client.post(
        "/auth/register",
        json={
            "email": "nodigit@example.com",
            "password": "OnlyLetters",  # no digits
            "name": "No",
            "surname": "Digit",
        },
    )
    assert res.status_code == 400
    assert "at least one number" in res.get_data(as_text=True)


def test_register_with_password_without_letters(client):
    res = client.post(
        "/auth/register",
        json={
            "email": "noletter@example.com",
            "password": "12345678",  # no letters
            "name": "No",
            "surname": "Letter",
        },
    )
    assert res.status_code == 400
    assert "at least one letter" in res.get_data(as_text=True)
