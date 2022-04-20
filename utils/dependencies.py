from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from models import User
from utils import Auth

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/auth/sign-in')


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    return await Auth.validate_token(token)


