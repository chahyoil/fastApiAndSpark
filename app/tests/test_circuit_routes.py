import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

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