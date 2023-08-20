from fastapi.testclient import TestClient
from main import app, update_json_file  # Assuming your FastAPI app is defined in my_app.py
from datetime import datetime
import json
import pytest
import os


client = TestClient(app)

# Load initial data from JSON file for testing
data_file_path = os.path.join(os.path.dirname(__file__), "Testing_data.json")

@pytest.fixture(scope="module")
def test_db_users():
    with open(data_file_path, 'r') as json_file:
        test_db_users = json.load(json_file)
    return test_db_users

def test_create_user(test_db_users):
    new_user_data = {
        "id": len(test_db_users) + 1,
        #"id": " ",
        "name": "Test new",
        "email": "test@example.com",
        "role": "user",
        "created_at": datetime.utcnow().isoformat(),
    }

    response = client.post("/users", json=new_user_data)
    assert response.status_code == 200
    assert response.json()["name"] == new_user_data["name"]

def test_get_user(test_db_users):
    user_id_to_test = 1
    response = client.get(f"/users/{user_id_to_test}")
    assert response.status_code == 200
    assert response.json()["id"] == user_id_to_test

def test_update_user(test_db_users):
    user_id_to_test = 20
    updated_user_data = {
        "id": user_id_to_test,
        "name": "Updated User",
        "email": "updated@example.com",
        "role": "admin",
        "created_at": test_db_users[user_id_to_test - 1]["created_at"],
    }

    response = client.put(f"/users/{user_id_to_test}", json=updated_user_data)
    assert response.status_code == 200
    assert response.json()["name"] == updated_user_data["name"]

def test_delete_user(test_db_users):
    user_id_to_test = 15
    response = client.delete(f"/users/{user_id_to_test}")
    assert response.status_code == 200
    assert response.json()["message"] == f"User with ID {user_id_to_test} has been deleted"
