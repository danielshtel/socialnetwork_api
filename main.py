import logging

import uvicorn
from fastapi import FastAPI, HTTPException, Query, status, Form, UploadFile, File
from ramda import *

from database import session, engine
from database import create_db_and_tables
from models.post import Post, PostBase, PostResponseView
from models.user import User, UserBase, UserUpdate
from settings import settings

logging.basicConfig(level=10)

logger = logging.getLogger(name='DB LOGGER')
app = FastAPI()


@app.on_event('startup')
async def on_startup():
    logger.info(msg='CREATING DB')
    # await create_db_and_tables(connection=engine)
    #


@app.on_event('shutdown')
async def on_shutdown():
    session.close()
    logger.info(msg='DB CONNECTION CLOSED')


@app.post("/files/")
async def create_file(file: bytes = File(...)):
    return {"file_size": len(file)}  # !TODO files uploads


@app.post("/uploadfile/")
async def create_upload_file(file: list[UploadFile]):
    return {"filename": file}  # !TODO files uploads


@app.post("/login/")
async def login(username: str = Form(...), password: str = Form(...)):
    return {"username": username}


@app.get('/user/all', response_model=list[User], tags=['user'])
async def users(limit: int | None = Query(None, lt=101, gt=0)):
    user_list = await User.get_all(session=session, limit=limit)
    if is_empty(user_list):
        raise HTTPException(status_code=400, detail='List of users is empty!')
    return user_list


@app.get('/user/{u_id}', response_model=UserUpdate, tags=['user'])
async def get_user(u_id: int):
    return await User.get_user(u_id=u_id, session=session)


@app.post('/user/', response_model=User, response_model_exclude={'password'}, status_code=status.HTTP_201_CREATED,
          tags=['user'])
async def create_user(user: UserBase):
    return await user.create(session=session)


@app.patch('/user/{u_id}', response_model=User, tags=['user'])
async def update_user(u_id: int, user: UserUpdate):
    db_user = await User.get_user(u_id=u_id, session=session)
    user_data = user.dict(exclude_unset=True)
    return await db_user.update_user(user_data, session)


@app.delete('/user/{u_id}/', tags=['user'])
async def delete_user(u_id: int):
    return await (await User.get_user(session=session, u_id=u_id)).delete_user(session=session)


@app.get('/post/{post_id}', response_model=PostResponseView, tags=['post'])
async def get_post(post_id: int):
    return await Post.get(session=session, post_id=post_id)


@app.get('/post/like/{post_id}', response_model=PostResponseView, tags=['post'])
async def like_post(post_id: int):
    return await Post.like(post_id=post_id, session=session)


@app.post('/post/', response_model=Post, tags=['post'])
async def create_post(post: PostBase):
    return await post.create(session=session)


if __name__ == '__main__':
    uvicorn.run('main:app', host=settings.server_host, port=settings.server_port, reload=True)
