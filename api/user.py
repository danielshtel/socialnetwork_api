from fastapi import APIRouter, HTTPException, Query, status, Response, Depends
from ramda import is_empty
from sqlmodel import Session

from database import engine
from models import User, UserUpdate, UserCreate, Post
from utils import get_current_user

router = APIRouter(
    prefix='/user',
)


@router.get('/all', response_model=list[User], tags=['user'])
async def users(limit: int | None = Query(None, lt=101, gt=0)):
    user_list = await User.get_all(limit=limit)
    if is_empty(user_list):
        raise HTTPException(status_code=400, detail='List of users is empty!')
    return user_list


@router.get('/', response_model=User, tags=['user'], response_model_exclude={'password'})
async def get_user(user: User = Depends(get_current_user)):
    return user


@router.post('/', response_model=User, response_model_exclude={'password'}, status_code=status.HTTP_201_CREATED,
             tags=['user'])
async def create_user(user: UserCreate):
    return await user.create()


@router.patch('/{user_id}', response_model=User, tags=['user'])
async def update_user(user_id: int, user: UserUpdate):
    db_user = await User.get_user(user_id=user_id)
    user_data = user.dict(exclude_unset=True)
    return await db_user.update_user(user_data)


@router.delete('/{user_id}',
               tags=['user'],
               status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int):
    await (await User.get_user(user_id=user_id)).delete_user()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get('/posts/{user_id}', response_model=list[Post], response_model_exclude={'user_id'})
async def get_posts(user_id: int):
    with Session(engine) as session:
        user = session.get(User, user_id)
        return user.posts
