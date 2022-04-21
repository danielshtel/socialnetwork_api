from fastapi import APIRouter, HTTPException, Query, status, Response, Depends
from ramda import is_empty
from sqlmodel import Session

from database import engine
from models import User, UserUpdate, Post
from utils import get_current_user

router = APIRouter(
    prefix='/user',
    tags=['user']
)


@router.get('/all', response_model=list[User])
async def users(limit: int | None = Query(None, lt=101, gt=0)):
    user_list = await User.get_all(limit=limit)
    if is_empty(user_list):
        raise HTTPException(status_code=400, detail='List of users is empty!')
    return user_list


@router.get('/', response_model=User, response_model_exclude={'password'})
async def get_user(user: User = Depends(get_current_user)):
    return user


@router.patch('/', response_model=User, response_model_exclude={'password'})
async def update_user(user_data: UserUpdate, user: User = Depends(get_current_user)):
    db_user = await User.get_user(user_id=user.id)
    user_dict = user_data.dict(exclude_unset=True)
    return await db_user.update_user(user_dict)


@router.delete('/{user_id}',
               tags=['user'],
               status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user: User = Depends(get_current_user)):
    await (await User.get_user(user_id=user.id)).delete_user()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get('/posts', response_model=list[Post], response_model_exclude={'user_id'})
async def get_posts(user_data: User = Depends(get_current_user)):
    with Session(engine) as session:
        user = session.get(User, user_data.id)
        if is_empty(user.posts):
            exception = HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'User {user.username} doesn\'t have any posts yet'
            )
            raise exception
        return user.posts
