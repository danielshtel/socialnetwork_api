from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm

from models import UserCreate, Token
from utils import Auth

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/sign-up', response_model=Token)
async def sign_up(user_data: UserCreate, auth: Auth = Depends()):
    return await auth.register_user(user_data)


@router.post('/sign-in', response_model=Token)
async def sign_in(form_data: OAuth2PasswordRequestForm = Depends(), auth: Auth = Depends()):
    return await auth.authenticate_user(username=form_data.username, password=form_data.password)
