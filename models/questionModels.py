from sqlalchemy import Column, Integer, String
from database.db import Base
from pydantic import BaseModel


class Question(Base):
    __tablename__ = 'questions'

    questionID = Column(Integer, primary_key=True, index=True)
    question = Column(String)
    answer = Column(String)

    class Config:
        schema_extra = {
            "Contoh": {
                "question": "Gender kamu saat ini?",
                "answer": "1 (Laki-laki) 2 (Perempuan) 3 (Hehe)"
            }
        }


class QuestionSchema(BaseModel):
    question: str
    answer: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "question": "Gender kamu saat ini?",
                "answer": "1 (Laki-laki) 2 (Perempuan) 3 (Hehe)"
            }
        }


class QuestionShow(BaseModel):
    questionID: int
    question: str
    answer: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "questionID": 1,
                "question": "Gender kamu saat ini?",
                "answer": "1 (Laki-laki) 2 (Perempuan) 3 (Hehe)"
            }
        }


class QuestionUpdate(BaseModel):
    question: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "question": "Gender kamu saat ini?",
            }
        }
