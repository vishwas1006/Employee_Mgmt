import uuid
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

AUTH_HEADERS = {
    "Authorization": "Bearer my-secret-token"
}


def test_create_employee():
    unique_email = f"bob_{uuid.uuid4()}@example.com"

    response = client.post(
        "/api/employees/",
        headers=AUTH_HEADERS,
        json={
            "name": "Bob",
            "email": unique_email,
            "department": "HR",
            "role": "Manager"
        }
    )

    assert response.status_code == 201


def test_duplicate_email():
    email = f"dup_{uuid.uuid4()}@example.com"

    # First create
    client.post(
        "/api/employees/",
        headers=AUTH_HEADERS,
        json={
            "name": "Bob",
            "email": email
        }
    )

    # Duplicate create
    response = client.post(
        "/api/employees/",
        headers=AUTH_HEADERS,
        json={
            "name": "Bob",
            "email": email
        }
    )

    assert response.status_code == 400


def test_get_non_existing_employee():
    response = client.get(
        "/api/employees/99999",
        headers=AUTH_HEADERS
    )

    assert response.status_code == 404


def test_update_employee():
    response = client.put(
        "/api/employees/1",
        headers=AUTH_HEADERS,
        json={"role": "Lead"}
    )

    assert response.status_code in [200, 404]


def test_delete_employee():
    response = client.delete(
        "/api/employees/1",
        headers=AUTH_HEADERS
    )

    assert response.status_code in [204, 404]


def test_auth_required():
    response = client.get("/api/employees/")
    assert response.status_code == 401
