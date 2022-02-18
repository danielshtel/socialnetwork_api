import os
from typing import List

import uvicorn
from fastapi import FastAPI
from sqlmodel import create_engine, Session

from models.user import User, create_db_and_tables, UserBase

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

engine = create_engine(f'sqlite:///{ROOT_DIR}/api.db')

session = Session(engine)
app = FastAPI()


@app.on_event('startup')
async def on_startup():
    await create_db_and_tables(connection=engine)


@app.get('/login')
async def login():
    pass


@app.post('/create_user/', response_model=User)
async def create_user(user: UserBase):
    return await user.create(session=session)


@app.get('/users', response_model=List[User])
async def users():
    user_list = await User.get_list(session=session)
    return user_list


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=80, reload=True)
