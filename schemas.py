from fastapi import FastAPI
from pydantic import BaseModel


class UserRegister(BaseModel):
    username: str
    phone_number: str
    password: str

class UserLogin(BaseModel):
    username: str
    phone_number: str
    password: str

class RoomCreate(BaseModel):
    name: str
    description: str