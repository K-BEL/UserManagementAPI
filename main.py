from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import datetime
import json

app = FastAPI()

# Data model for User
class User(BaseModel):
    id: int
    name: str
    email: str
    role: str
    created_at: datetime

# Convert a user dictionary's created_at field to ISO format
def user_dict_to_json(user_dict):
    user_dict_copy = user_dict.copy()
    user_dict_copy["created_at"] = user_dict_copy["created_at"].isoformat()
    return user_dict_copy

# Convert a JSON user dictionary's created_at field to a datetime object
def json_to_user_dict(json_user_dict):
    json_user_dict_copy = json_user_dict.copy()
    json_user_dict_copy["created_at"] = datetime.fromisoformat(json_user_dict_copy["created_at"])
    return json_user_dict_copy

# Load initial data from JSON file
db_users = []
data_file_path = r'C:\Users\LENOVO\Desktop\APIs_task\my_api\Testing_data.json'

with open(data_file_path, 'r') as json_file:
    db_users = [json_to_user_dict(user) for user in json.load(json_file)]

def update_json_file(data):
    with open(data_file_path, 'w') as json_file:
        json.dump([user_dict_to_json(user_dict) for user_dict in data], json_file, indent=4)

# Endpoint to retrieve all users
@app.get("/users", response_model=List[User])
def get_users():
    return db_users

@app.get("/users/{id}", response_model=User)
def get_user(id: int):
    user = next((user for user in db_users if user["id"] == id), None)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Endpoint to create a new user
@app.post("/users", response_model=User)
def create_user(user: User):
    user_dict = user.dict()
    user_dict["created_at"] = datetime.utcnow()
    user_dict["id"] = len(db_users) + 1
    db_users.append(user_dict)
    update_json_file(db_users)  # Update JSON file
    return user


# Endpoint to update an existing user by ID
@app.put("/users/{id}", response_model=User)
def update_user(id: int, updated_user: User):
    user_index = next((index for index, user in enumerate(db_users) if user["id"] == id), None)
    if user_index is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_users[user_index] = updated_user.dict()
    update_json_file(db_users)
    return updated_user

# Endpoint to delete a user by ID
@app.delete("/users/{id}", response_model=dict)
def delete_user(id: int):
    user_index = next((index for index, user in enumerate(db_users) if user["id"] == id), None)
    if user_index is None:
        raise HTTPException(status_code=404, detail="User not found")
    deleted_user = db_users.pop(user_index)
    update_json_file(db_users)
    return {"message": f"User with ID {id} has been deleted"}
