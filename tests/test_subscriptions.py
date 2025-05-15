from flask_jwt_extended import decode_token


def test_user_can_subscribe_and_get_active_plan(client):
    client.post(
        "/auth/register",
        json={
            "email": "user@example.com",
            "password": "StrongPass123",
            "name": "Test",
            "surname": "User",
        },
    )
    res = client.post(
        "/auth/login", json={"email": "user@example.com", "password": "StrongPass123"}
    )
    print(res.get_json())
    token = res.get_json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    client.post("/plans/", json={"name": "Pro", "price": 19.99, "duration_days": 60})

    res = client.post(
        "/subscriptions/subscribe", json={"email": "user@example.com", "plan_id": 1}
    )
    assert res.status_code == 201

    res = client.get("/subscriptions/active", headers=headers)
    assert res.status_code == 200
    assert res.get_json()["plan"] == "Pro"


def test_subscribe_with_invalid_user(client):
    client.post("/plans/", json={"name": "Basic", "price": 5.00, "duration_days": 15})
    res = client.post(
        "/subscriptions/subscribe", json={"email": "unknown@example.com", "plan_id": 1}
    )
    assert res.status_code == 404


def test_subscribe_with_invalid_plan(client):
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
        "/subscriptions/subscribe", json={"email": "user@example.com", "plan_id": 999}
    )
    assert res.status_code == 404


def test_get_active_subscription_without_token(client):
    res = client.get("/subscriptions/active")
    assert res.status_code == 401
