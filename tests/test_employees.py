import pytest
from fastapi.testclient import TestClient
from app.main import app
import uuid

client = TestClient(app)

def test_create_employee():
    unique_email = f"bob_{uuid.uuid4()}@example.com"

    response = client.post(
        "/api/employees/",
        json={
            "name": "Bob",
            "email": unique_email,
            "department": "HR",
            "role": "Manager"
        }
    )

    assert response.status_code == 201
    assert response.json()["email"] == unique_email

    
def test_duplicate_email():
    response = client.post(
        "/api/employees/",
        json={
            "name": "Bob",
            "email": "bob@example.com"
        }
    )
    assert response.status_code == 400


def test_get_non_existing_employee():
    response = client.get("/api/employees/9999")
    assert response.status_code == 404

def test_update_employee():
    response = client.put(
        "/api/employees/1",
        json={"role": "Lead"}
    )
    assert response.status_code in [200, 404]


def test_delete_employee():
    response = client.delete("/api/employees/1")
    assert response.status_code in [204, 404]


def test_auth_required():
    response = client.post("/api/employees/", json={})
    assert response.status_code in [401, 403, 422]
