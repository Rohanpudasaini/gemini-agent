def test_signup_and_login(client):
    # Signup
    res = client.post(
        "/signup", json={"email": "test@example.com", "password": "secret"}
    )
    assert res.status_code == 200
    assert res.json()["email"] == "test@example.com"

    # Login
    res = client.post(
        "/login", data={"username": "test@example.com", "password": "secret"}
    )
    assert res.status_code == 200
    token = res.json()["access_token"]
    assert token

    # Access protected route
    headers = {"Authorization": f"Bearer {token}"}
    res = client.get("/me", headers=headers)
    assert res.status_code == 200
    assert res.json()["email"] == "test@example.com"
