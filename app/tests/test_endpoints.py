import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "F1 Race Data API"}

def test_get_circuits():
    response = client.get("/api/circuits/")
    assert response.status_code == 200
    assert "circuits" in response.json()
    assert "total_count" in response.json()

def test_get_circuit_info():
    response = client.get("/api/circuits/1")
    assert response.status_code == 200
    assert "circuit_info" in response.json()
    assert "races" in response.json()

def test_get_circuit_races():
    response = client.get("/api/circuits/1/races")
    assert response.status_code == 200
    assert "circuit_races" in response.json()

def test_get_constructor_standings():
    response = client.get("/api/constructors/standings")
    assert response.status_code == 200
    assert "standings" in response.json()
    assert "total_count" in response.json()

def test_get_constructor_results():
    response = client.get("/api/constructors/1/results")
    assert response.status_code == 200
    assert "constructor_results" in response.json()

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

def test_get_races():
    response = client.get("/api/races/")
    assert response.status_code == 200
    assert "races" in response.json()
    assert "total_count" in response.json()

def test_get_race_details():
    response = client.get("/api/races/1")
    assert response.status_code == 200
    assert "race_details" in response.json()

def test_get_race_results():
    response = client.get("/api/races/1/results")
    assert response.status_code == 200
    assert "race_results" in response.json()

def test_get_fastest_laps():
    response = client.get("/api/races/1/fastest-laps")
    assert response.status_code == 200
    assert "fastest_laps" in response.json()