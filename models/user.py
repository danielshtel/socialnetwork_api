from datetime import date

from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import EmailStr
from sqlmodel import Field, SQLModel, select

from database import SessionMixin

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class UserBase(SessionMixin, SQLModel):
    username: str = Field(..., index=True,
                          sa_column_kwargs={'unique': True})  # https://github.com/tiangolo/sqlmodel/issues/65
    email: EmailStr = Field(..., index=True, sa_column_kwargs={'unique': True})
    age: date = Field(..., index=True)
    hashed_password: str = Field(...)
    disabled: bool | None = Field(None)

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

    @staticmethod
    async def __fake_decode_user(token: str):
        return await User.get_by_username(token)

    @classmethod
    async def get_current_user(cls, token: str = Depends(oauth2_scheme)):
        user = await cls.__fake_decode_user(token)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid auth credentials',
                headers={'WWW-Authenticate': 'Bearer'}
            )
        return user


class UserUpdate(SQLModel):
    username: str | None = None
    email: EmailStr | None = None
    age: date | None = None
