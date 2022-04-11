from datetime import date

from fastapi import HTTPException
from pydantic import EmailStr
from sqlmodel import Field, SQLModel, select

from database import SessionMixin


class UserBase(SessionMixin, SQLModel):
    name: str = Field(..., index=True)
    email: EmailStr = Field(..., index=True)
    age: date = Field(..., index=True)
    password: str = Field(...)

    class Config:
        schema_extra = {'example': {
            'name': 'User name',
            'age': '2022-12-01',
            'email': 'example@mail.com',
            'password': '123456pass'
        }}
        orm_mode = True

    async def create(self):
        with self._session:
            user = User.from_orm(self)
            self._session.add(user)
            self._session.commit()
            self._session.refresh(user)
            return user


class User(UserBase, table=True):
    __tablename__ = 'user'

    id: int = Field(default=None, primary_key=True)

    @classmethod
    async def get_all(cls, limit: int = 10, offset: int = 0) -> list:
        with cls._session:
            return cls._session.exec(select(cls).offset(offset).limit(limit)).all()

    @classmethod
    async def get_user(cls, user_id: int):
        with cls._session:
            user = cls._session.get(cls, user_id)
            if not user:
                raise HTTPException(status_code=404, detail='User does not exist')
            return user

    async def update_user(self, user_data):
        with self._session:
            for key, value in user_data.items():
                setattr(self, key, value)
            self._session.add(self)
            self._session.commit()
            self._session.refresh(self)
            return self

    async def delete_user(self):
        with self._session:
            self._session.delete(self)
            self._session.commit()


class UserUpdate(SQLModel):
    name: str | None = None
    email: EmailStr | None = None
    age: date | None = None
