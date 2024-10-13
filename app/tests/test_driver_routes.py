import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_drivers():
    response = client.get("/api/drivers/")
    assert response.status_code == 200
    assert "drivers" in response.json()
    assert "total_count" in response.json()

def test_get_driver_details():
    response = client.get("/api/drivers/1")
    assert response.status_code == 200
    assert "driver_details" in response.json()

def test_get_driver_standings():
    response = client.get("/api/drivers/1/standings")
    assert response.status_code == 200
    assert "driver_standings" in response.json()