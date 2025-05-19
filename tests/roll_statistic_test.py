import pytest
import requests
from typing import Dict, Any

from sqlalchemy import text

from tests.config import engine, API_PORT, API_HOST

API_URL = f"{API_HOST}:{API_PORT}/api/v1/roll_statistic"


@pytest.fixture
def headers():
    return {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }


def validate_statistics_response(response_data: Dict[str, Any]) -> None:
    """Helper function to validate the statistics response structure"""
    assert isinstance(response_data, dict)
    assert set(response_data.keys()) == {"result", "error"}

    # Validate result object
    assert isinstance(response_data["result"], dict)
    assert set(response_data["result"].keys()) == {"all_count_roll", "all_awg_roll"}
    assert isinstance(response_data["result"]["all_count_roll"], int)
    assert isinstance(response_data["result"]["all_awg_roll"], (int, float))

    assert response_data["error"] is None


def test_get_statistics_success(headers):
    """Test successful retrieval of roll statistics"""
    response = requests.get(
        API_URL,
        headers=headers
    )

    assert response.status_code == 200
    response_data = response.json()

    validate_statistics_response(response_data)

    assert response_data["result"]["all_count_roll"] >= 0
    assert response_data["result"]["all_awg_roll"] >= 0


def test_statistics_database_integration(headers):
    """Test successful retrieval of roll statistics"""
    response = requests.get(
        API_URL,
        headers=headers
    )

    assert response.status_code == 200
    result = response.json()["result"]
    all_awg_roll = result["all_awg_roll"]

    with engine.connect() as connection:
        query = text("SELECT AVG(value) FROM roll_events")
        avg_result = connection.execute(query).scalar()

        assert avg_result is not None
        avg_result = float(avg_result)
        assert round(avg_result, 5) == round(all_awg_roll, 5)


def test_unsupported_methods(headers):
    """Test that POST, PUT, DELETE methods are not allowed"""
    for method in ["POST", "PUT", "DELETE", "PATCH"]:
        response = requests.request(
            method,
            API_URL,
            headers=headers
        )
        assert response.status_code == 404
