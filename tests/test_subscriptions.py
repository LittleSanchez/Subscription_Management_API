from flask_jwt_extended import decode_token


def test_subscribe_flow(client):
    client.post(
        "/auth/register",
        json={
            "email": "user@example.com",
            "password": "1234",
            "name": "Test",
            "surname": "User",
        },
    )
    res = client.post(
        "/auth/login", json={"email": "user@example.com", "password": "1234"}
    )
    token = res.get_json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    client.post("/plans/", json={"name": "Pro", "price": 19.99, "duration_days": 60})

    res = client.post(
        "/subscriptions/subscribe", json={"email": "user@example.com", "plan_id": 1}
    )
    assert res.status_code == 201

    res = client.get("/subscriptions/active", headers=headers)
    assert res.status_code == 200
    data = res.get_json()
    assert data["plan"] == "Pro"
