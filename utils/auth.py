from datetime import datetime, timedelta

from fastapi import HTTPException, status
from jose import jwt, JWTError
from passlib.hash import bcrypt
from pydantic import ValidationError

from database import SessionMixin
from models import User, Token, UserCreate
from settings import settings


class Auth(SessionMixin):

    @classmethod
    async def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.verify(plain_password, hashed_password)

    @classmethod
    async def hash_password(cls, password: str) -> str:
        return bcrypt.hash(password)

    @classmethod
    async def validate_token(cls, token: str) -> User:
        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials',
            headers={'WWW-Authenticate': 'Bearer'}

        )
        try:
            payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])

        except JWTError:
            raise exception from None
        user_data = payload.get('user')

        try:
            user = User.parse_obj(user_data)
        except ValidationError:
            raise exception from None
        return user

    @classmethod
    async def create_token(cls, user: User) -> Token:
        user_data = User.from_orm(user)
        now = datetime.utcnow()
        payload = {
            'iat': now,
            'nbf': now,
            'exp': now + timedelta(seconds=settings.jwt_expiration),
            'sub': str(user_data.id),
            'user': user_data.dict()
        }
        token = jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)
        return Token(access_token=token)

    async def register_user(self, user_data: UserCreate) -> Token:
        user = User(
            email=user_data.email,
            username=user_data.username,
            age=user_data.age,
            password=(await self.hash_password(user_data.password))
        )
        with self._session as session:
            session.add(user)
            session.commit()
            session.refresh(user)

        return await self.create_token(user)

    async def authenticate_user(self, username: str, password: str) -> Token:
        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'}

        )
        user = await User.get_by_username(username)
        if not user:
            raise exception from None
        if not await self.verify_password(password, user.password):
            raise exception from None
        return await self.create_token(user)
