from sqlalchemy import Column, Integer, String
from database.db import Base
from pydantic import BaseModel, EmailStr, conint
from typing import Optional


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String)
    nama = Column(String)
    password = Column(String)

    class Config:
        schema_extra = {
            "Contoh": {
                "email": "contoh123@mailmail.com",
                "nama": "Agus",
                "password": "ashiapp!!",
            }
        }


class UserSchema(BaseModel):
    email: EmailStr
    nama: str
    password: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "email": "contoh123@mailmail.com",
                "nama": "Agus",
                "password": "ashiapp!!",
            }
        }


class ShowUser(BaseModel):
    email: EmailStr
    nama: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "email": "contoh123@mailmail.com",
                "nama": "Agus"
            }
        }


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None