def test_register_and_login(client):

    res = client.post(
        "/auth/register",
        json={
            "email": "user@example.com",
            "password": "1234",
            "name": "Test",
            "surname": "User",
        },
    )
    assert res.status_code == 201

    res = client.post(
        "/auth/login", json={"email": "user@example.com", "password": "1234"}
    )
    assert res.status_code == 200
    data = res.get_json()
    assert "access_token" in data
