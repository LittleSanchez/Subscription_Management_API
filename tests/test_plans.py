def test_create_and_retrieve_subscription_plans(client):
    res = client.post(
        "/plans/", json={"name": "Basic", "price": 9.99, "duration_days": 30}
    )
    assert res.status_code == 201

    res = client.get("/plans/")
    assert res.status_code == 200
    plans = res.get_json()
    assert any(plan["name"] == "Basic" for plan in plans)


def test_create_plan_with_missing_fields(client):
    res = client.post("/plans/", json={"name": "Pro"})
    assert res.status_code == 400


def test_create_duplicate_plan(client):
    client.post("/plans/", json={"name": "Basic", "price": 5.00, "duration_days": 15})
    res = client.post(
        "/plans/", json={"name": "Basic", "price": 10.00, "duration_days": 30}
    )
    assert res.status_code == 400
