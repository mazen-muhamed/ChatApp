from fastapi import FastAPI
from schemas import UserRegister, UserLogin, RoomCreate
from fastapi import HTTPException, status, Depends, WebSocket, WebSocketException, WebSocketDisconnect
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import text
import database
from database import get_db
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.requests import Request



app = FastAPI(title="ChatApp")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="Templates")


@app.get("/")
def root(request: Request):
    return templates.TemplateResponse(request, "login.html")


@app.get("/login.html")
def login_page(request: Request):
    return templates.TemplateResponse(request, "login.html")


@app.get("/chat.html")
def chat_page(request: Request):
    return templates.TemplateResponse(request, "chat.html")




@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    result = db.execute(
        text("SELECT id, username, phone_number, created_at FROM users")
    ).fetchall()
    return [dict(row._mapping) for row in result]


## Authentication : Register , Login


@app.post("/register", status_code=status.HTTP_201_CREATED)
def register(payload: UserRegister, db: Session = Depends(get_db)):
    existing = db.execute(
        text("SELECT id FROM users WHERE phone_number = :phone_number"),
        {"phone_number": payload.phone_number}
    ).fetchone()

    if existing:
        raise HTTPException(400, "Phone Number Already exist")

    db.execute(
        text("""
            INSERT INTO users (username, phone_number, hashed_password)
            VALUES (:username, :phone_number, :hashed_password)
        """),
        {
            "username": payload.username,
            "phone_number": payload.phone_number,
            "hashed_password": payload.password
        }
    )
    db.commit()
    return {"message": "✅ User Registered"}
    
    
@app.post("/login")
def login(payload: UserLogin, db: Session = Depends(get_db)):
    user = db.execute(
        text("SELECT * FROM users WHERE phone_number = :phone_number"),
        {"phone_number": payload.phone_number}
    ).fetchone()
    
    if not user or user.hashed_password != payload.password:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Incorrect phone number or password")
    if not user.is_active:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Account is inactive")

    return {"message": "✅ Login successful", "username": user.username}
    

@app.post("/rooms", status_code=status.HTTP_201_CREATED)
def create_room(
    room: RoomCreate,
    db: Session = Depends(get_db)
):
    existing = db.execute(
        # query
        text("SELECT * FROM rooms WHERE name = :name"),
        {
            "name": room.name
        }
    ).fetchone()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Room already exists"
        )

    db.execute(
        # Write ur query
        text("""
              INSERT INTO rooms (name, description) 
              VALUES (:name, :description)
        """),
        {
            "name": room.name,
            "description": room.description
        }
    )

    db.commit()

    return {
        "message": "Room Created Successfully",
        "room": {
            "name": room.name,
            "description": room.description
        }
    }


@app.get("/rooms")
def get_rooms(db: Session = Depends(get_db)):
    result = db.execute(
        #write ur query
        text("""
            SELECT * FROM rooms
         """)
    ).fetchall()

    return [dict(row._mapping) for row in result]


# app.websocket("/ws/{room_id}")(websocket_endpoint)
