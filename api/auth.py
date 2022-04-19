from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from models import UserAuth, User

router = APIRouter()


def fake_hash_pass(password: str) -> str:
    return 'fakehash' + password


@router.post('/token', tags=['auth'])
async def login(data: OAuth2PasswordRequestForm = Depends()):
    user_dict = await User.get_by_username(username=data.username)
    if not user_dict:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Incorrect username or password')
    user = UserAuth(**user_dict.dict())
    hashed_password = fake_hash_pass(data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail='Incorrect username or password')
    return {'access_token': user.username, 'token_type': 'bearer'}


