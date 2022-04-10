from fastapi import APIRouter, HTTPException, Query, status
from ramda import is_empty

from database import session
from models import User
from models.user import UserUpdate, UserBase

router = APIRouter(
    prefix='/user',
)


@router.get('/all', response_model=list[User], tags=['user'])
async def users(limit: int | None = Query(None, lt=101, gt=0)):
    user_list = await User.get_all(session=session, limit=limit)
    if is_empty(user_list):
        raise HTTPException(status_code=400, detail='List of users is empty!')
    return user_list


@router.get('/{u_id}', response_model=UserUpdate, tags=['user'])
async def get_user(u_id: int):
    return await User.get_user(u_id=u_id, session=session)


@router.post('/', response_model=User, response_model_exclude={'password'}, status_code=status.HTTP_201_CREATED,
             tags=['user'])
async def create_user(user: UserBase):
    return await user.create(session=session)


@router.patch('/{u_id}', response_model=User, tags=['user'])
async def update_user(u_id: int, user: UserUpdate):
    db_user = await User.get_user(u_id=u_id, session=session)
    user_data = user.dict(exclude_unset=True)
    return await db_user.update_user(user_data, session)


@router.delete('/{u_id}', response_model=User, response_model_exclude={'password'}, tags=['user'])
async def delete_user(u_id: int):
    return await (await User.get_user(session=session, u_id=u_id)).delete_user(session=session)
