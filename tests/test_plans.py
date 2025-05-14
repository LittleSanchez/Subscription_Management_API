def test_create_and_list_plans(client):
    res = client.post(
        "/plans/", json={"name": "Basic", "price": 9.99, "duration_days": 30}
    )
    assert res.status_code == 201

    res = client.get("/plans/")
    assert res.status_code == 200
    data = res.get_json()
    assert any(plan["name"] == "Basic" for plan in data)
