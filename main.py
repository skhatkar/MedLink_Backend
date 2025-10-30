from fastapi import FastAPI
from fastapi.responses import JSONResponse
from datetime import datetime

app = FastAPI()

@app.post("/login")
def login(username: str, password: str):
    # Temporary test user (we'll connect to DB later)
    if username == "Shubh" and password == "ShubhPassword123":
        response = {
            "timestamp": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            "status": "OK",
            "message": "Login successful",
            "data": {
                "roleId": 1,
                "roleName": "Super Admin",
                "username": "Shubh"
            }
        }
    else:
        response = {
            "timestamp": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            "status": "FAIL",
            "message": "Invalid username or password",
            "data": None
        }

    return JSONResponse(content=response)

import json
import os

USERS_FILE = "users.json"

# Create file if it doesn't exist
if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, "w") as f:
        json.dump([], f)


@app.post("/register")
def register(username: str, password: str, roleName: str = "User"):
    # Load existing users
    with open(USERS_FILE, "r") as f:
        users = json.load(f)

    # Check if username already exists
    for u in users:
        if u["username"] == username:
            return {
                "timestamp": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
                "status": "FAIL",
                "message": "Username already exists",
                "data": None
            }

    # Create new user data
    new_user = {
        "username": username,
        "password": password,   # (we'll encrypt later)
        "roleId": len(users) + 1,
        "roleName": roleName
    }

    # Save user
    users.append(new_user)
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

    return {
        "timestamp": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        "status": "OK",
        "message": "User registered successfully",
        "data": {
            "username": username,
            "roleId": new_user["roleId"],
            "roleName": roleName
        }
    }
