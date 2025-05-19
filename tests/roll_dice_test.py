import requests
from sqlalchemy import text

from tests.config import engine, API_PORT, API_HOST

API_URL = f"{API_HOST}:{API_PORT}/api/v1/roll_dice"

def test_roll_dice_success():
    response = requests.post(API_URL)

    assert response.status_code == 200
    data = response.json()
    assert "result" in data
    assert isinstance(data["result"], int)
    assert 1 <= data["result"] <= 6
    assert data["error"] is None
    assert response.headers["Content-Type"] == "application/json; charset=utf-8"


def test_roll_dice_database_integration():

    response = requests.post(API_URL)
    assert response.status_code == 200
    data = response.json()
    result = data["result"]

    # Подключение к базе данных
    with engine.connect() as connection:
        query = text("SELECT value FROM roll_events WHERE value = :result LIMIT 1")
        result_in_db = connection.execute(query, {"result": result}).fetchone()

        assert result_in_db is not None
        assert result_in_db[0] == result