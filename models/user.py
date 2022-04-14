from datetime import date

from fastapi import HTTPException
from pydantic import EmailStr
from sqlmodel import Field, SQLModel, select

from database import SessionMixin


class UserBase(SessionMixin, SQLModel):
    username: str = Field(..., index=True,
                          sa_column_kwargs={'unique': True})  # https://github.com/tiangolo/sqlmodel/issues/65
    email: EmailStr = Field(..., index=True, sa_column_kwargs={'unique': True})
    age: date = Field(..., index=True)
    hashed_password: str = Field(...)

    class Config:
        schema_extra = {'example': {
            'username': 'username',
            'age': '2022-12-01',
            'email': 'example@mail.com',
            'hashed_password': '123456'
        }}
        orm_mode = True


class UserAuth(UserBase):
    hashed_password: str


class UserCreate(UserBase):

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
    async def get_by_username(cls, username: str):
        user = cls._session.exec(select(cls).where(cls.username == username)).first()
        return user

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
    username: str | None = None
    email: EmailStr | None = None
    age: date | None = None
