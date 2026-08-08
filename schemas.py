from fastapi import FastAPI
from pydantic import BaseModel


class UserRegister(BaseModel):
    userName: str
    phoneNumber: int
    password: str

class UserLogin(BaseModel):
    userName: str
    PhoneNumber: int
    password: str

class RoomCreate(BaseModel):
    name: str
    description: str