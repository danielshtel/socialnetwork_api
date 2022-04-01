import os
from typing import List

import uvicorn
from fastapi import FastAPI, HTTPException, Query
from sqlmodel import create_engine, Session
from ramda import *
from models.user import User, create_db_and_tables, UserBase, UserUpdate

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

engine = create_engine(f'sqlite:///{ROOT_DIR}/api.db')

session = Session(engine)
app = FastAPI()


@app.on_event('startup')
async def on_startup():
    await create_db_and_tables(connection=engine)


@app.on_event('shutdown')
async def on_shutdown():
    session.close()


@app.get('/login')
async def login():
    pass


@app.post('/user/create/', response_model=User)
async def create_user(user: UserBase):
    return await user.create(session=session)


@app.get('/user/all', response_model=List[User])
async def users(limit: int = Query(default=20, lt=101, gt=0)):
    user_list = await User.get_all(session=session, limit=limit)
    if is_empty(user_list):
        raise HTTPException(status_code=400, detail='List of users is empty!')
    return user_list


@app.get('/user/{u_id}', response_model=UserUpdate)
async def get_user(u_id: int):
    return await User.get_user(u_id=u_id, session=session)


@app.patch('/user/{u_id}', response_model=User)
async def update_user(u_id: int, user: UserUpdate):
    db_user = await User.get_user(u_id=u_id, session=session)
    user_data = user.dict(exclude_unset=True)
    for key, value in user_data.items():
        setattr(db_user, key, value)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user  # !TODO logic remove && sessions.


@app.delete('/user/{u_id}/')
async def delete_user(u_id: int):
    return await (await User.get_user(session=session, u_id=u_id)).delete_user(session=session)


if __name__ == '__main__':
    uvicorn.run('main:app', host='localhost', port=8082, reload=True)
