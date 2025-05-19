import pytest
import requests

from tests.config import API_HOST, API_PORT

API_URL = f"{API_HOST}:{API_PORT}/ping"

@pytest.fixture
def headers():
    return {
        "Accept": "application/json"
    }


def test_ping_endpoint(headers):
    """Test basic ping endpoint functionality"""
    response = requests.get(
        API_URL,
        headers=headers
    )

    assert response.status_code == 200

    assert "application/json" in response.headers["Content-Type"]

    response_data = response.json()
    assert set(response_data.keys()) == {"result"}
    assert response_data["result"] == "I am alive"


def test_ping_with_unsupported_methods(headers):
    """Test that only GET method is allowed"""
    for method in ["POST", "PUT", "DELETE", "PATCH"]:
        response = requests.request(
            method,
            API_URL,
            headers=headers
        )
        assert response.status_code == 404
