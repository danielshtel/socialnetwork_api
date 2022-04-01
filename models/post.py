from typing import Optional

from fastapi import HTTPException
from pydantic import EmailStr
from sqlmodel import Field, SQLModel, Session, create_engine, select


class PostBase(SQLModel):
    content: str = Field(default=None)
    like: int = Field(default=None)


class Post(PostBase, table=True):
    __tablename__ = 'post'
    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key='user.id')


