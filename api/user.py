from fastapi import APIRouter, HTTPException, Query, status, Response
from ramda import is_empty

from models import User, UserUpdate, UserCreate

router = APIRouter(
    prefix='/user',
)


@router.get('/all', response_model=list[User], tags=['user'])
async def users(limit: int | None = Query(None, lt=101, gt=0)):
    user_list = await User.get_all(limit=limit)
    if is_empty(user_list):
        raise HTTPException(status_code=400, detail='List of users is empty!')
    return user_list


@router.get('/{user_id}', response_model=UserUpdate, tags=['user'])
async def get_user(user_id: int):
    return await User.get_user(user_id=user_id)


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
