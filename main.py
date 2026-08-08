from fastapi import FastAPI
from schemas import UserRegister
from schemas import UserLogin
from schemas import RoomCreate
from fastapi import HTTPException , status, Depends, WebSocket, WebSocketException, WebSocketDisconnect
from fastapi import WebSocket
from datetime import datetime
from websocket import websocket_endpoint



app = FastAPI()

users = []
rooms = []
active_connections = {}

@app.get("/")
def home():
    return {"message": "Chat API is running"}

@app.get("/users")
def get_users():
    return users

@app.post("/register")
def register(user: UserRegister, status_code=status.HTTP_201_CREATED):
    for existing_user in users:

        if existing_user.email == user.email:
            raise HTTPException(
                status_code=400,
                detail="Email already exists"
            )

    users.append(user)

    return {
        "message": "User registered successfully",
        "data": user
    }

@app.post("/token")
def login(login_data: UserLogin):
    for user in users:

        if (
            user.email == login_data.email
            and user.password == login_data.password
        ):

            return {
                "message": "Login Successful"
            }

    raise HTTPException(
        status_code=401,
        detail="Invalid Email or Password"
    )

@app.post("/rooms")
def create_room(room: RoomCreate):
    for existing_room in rooms:

        if existing_room.name == room.name:
            raise HTTPException(
                status_code=400,
                detail="Room already exists"
            )

    rooms.append(room)

    return {
        "message": "Room Created Successfully",
        "room": room
    }

@app.get("/rooms")
def get_rooms():

    return rooms


app.websocket("/ws/{room_id}")(websocket_endpoint)
