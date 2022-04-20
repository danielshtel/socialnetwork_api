from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from models import User, UserCreate, Token

router = APIRouter(prefix='/auth')


@router.post('/sign-up', tags=['auth'], response_model=Token)
async def sign_up(user_data: UserCreate):
    pass


@router.post('/sign-in', tags=['auth'], response_model=Token)
async def sign_in(form_data: OAuth2PasswordRequestForm = Depends()):
    pass
