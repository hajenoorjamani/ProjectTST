from sqlalchemy import Column, Integer, String
from database.db import Base
from pydantic import BaseModel, EmailStr, conint
from typing import Optional


class User(Base):
    __tablename__ = 'users'

    userID = Column(Integer, primary_key=True, index=True)
    email = Column(String)
    nama = Column(String)
    password = Column(String)
    recommendation = Column(Integer)

    class Config:
        schema_extra = {
            "Contoh": {
                "email": "admin@gmail.com",
                "nama": "Admin",
                "password": "pass123",
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
                "email": "admin@gmail.com",
                "nama": "Admin",
                "password": "pass123",
            }
        }


class ShowUser(BaseModel):
    email: EmailStr
    nama: str
    recommendation: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "email": "admin@gmail.com",
                "nama": "Admin",
                "recommendation":"1"
            }
        }


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


class AnswerSchema(BaseModel):
    question_answer_1: conint(gt=-1, lt=4)
    question_answer_2: conint(gt=-1, lt=4)
    question_answer_3: conint(gt=-1, lt=4)
    question_answer_4: conint(gt=-1, lt=4)
    question_answer_5: conint(gt=-1, lt=4)
    
    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "question_answer_1": 3,
                "question_answer_2": 1,
                "question_answer_3": 3,
                "question_answer_4": 2,
                "question_answer_5": 1
            }
        }
