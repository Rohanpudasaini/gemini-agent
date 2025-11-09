import pytest


@pytest.mark.usefixtures("client")
class TestAuthFlow:
    def test_signup(self, client):
        res = client.post(
            "/signup", json={"email": "test@example.com", "password": "secret"}
        )
        assert res.status_code == 200

        assert res.json()["email"] == "test@example.com"

    def test_login(self, client):
        res = client.post(
            "/login", data={"username": "test@example.com", "password": "secret"}
        )
        assert res.status_code == 200
        token = res.json()["access_token"]
        assert token
        pytest.token = token  # type: ignore # Store token for later tests

    def test_protected_route(self, client):
        # Access protected route
        headers = {"Authorization": f"Bearer {pytest.token}"}  # type: ignore
        res = client.get("/me", headers=headers)
        assert res.status_code == 200
        assert res.json()["email"] == "test@example.com"
