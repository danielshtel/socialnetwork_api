from datetime import date

from fastapi import HTTPException
from pydantic import EmailStr
from sqlmodel import Field, SQLModel, Session, select


class UserBase(SQLModel):
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

    async def create(self, session: Session):
        with session:
            user = User.from_orm(self)
            session.add(user)
            session.commit()
            session.refresh(user)
            return user


class User(UserBase, table=True):
    __tablename__ = 'user'

    id: int = Field(default=None, primary_key=True)

    class Config:
        orm_mode = True

    @classmethod
    async def get_all(cls, session: Session, limit: int = 10, offset: int = 0) -> list:
        return session.exec(select(cls).offset(offset).limit(limit)).all()

    @classmethod
    async def get_user(cls, session: Session, u_id: int):
        user = session.get(cls, u_id)
        if not user:
            raise HTTPException(status_code=404, detail='User does not exist')
        return user

    async def update_user(self, user_data, session: Session):
        for key, value in user_data.items():
            setattr(self, key, value)
        session.add(self)
        session.commit()
        session.refresh(self)
        return self

    async def delete_user(self, session: Session):
        session.delete(self)
        session.commit()
        return self


class UserUpdate(SQLModel):
    name: str | None = None
    email: EmailStr | None = None
    age: date | None = None
