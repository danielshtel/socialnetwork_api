import logging

import uvicorn
from fastapi import FastAPI, HTTPException, Query
from ramda import *

from db.db_init import create_db_and_tables
from db.config import session, engine
from models.post import Post, PostBase, PostResponseView
from models.user import User, UserBase, UserUpdate

logging.basicConfig(level=10)

logger = logging.getLogger(name='    ')
app = FastAPI()


@app.on_event('startup')
async def on_startup():
    logger.info(msg='CREATING DB')
    await create_db_and_tables(connection=engine)


@app.on_event('shutdown')
async def on_shutdown():
    session.close()
    logger.info(msg='DB CONNECTION CLOSED')


@app.get('/login')
async def login():
    pass


@app.get('/user/all', response_model=list[User])
async def users(limit: int | None = Query(None, lt=101, gt=0)):
    user_list = await User.get_all(session=session, limit=limit)
    if is_empty(user_list):
        raise HTTPException(status_code=400, detail='List of users is empty!')
    return user_list


@app.get('/user/{u_id}', response_model=UserUpdate)
async def get_user(u_id: int):
    return await User.get_user(u_id=u_id, session=session)


@app.post('/user/', response_model=User)
async def create_user(user: UserBase):
    return await user.create(session=session)


@app.patch('/user/{u_id}', response_model=User)
async def update_user(u_id: int, user: UserUpdate):
    db_user = await User.get_user(u_id=u_id, session=session)
    user_data = user.dict(exclude_unset=True)
    return await db_user.update_user(user_data, session)


@app.delete('/user/{u_id}/')
async def delete_user(u_id: int):
    return await (await User.get_user(session=session, u_id=u_id)).delete_user(session=session)


@app.get('/post/{post_id}', response_model=PostResponseView)
async def get_post(post_id: int):
    return await Post.get(session=session, post_id=post_id)


@app.get('/post/like/{post_id}', response_model=PostResponseView)
async def like_post(post_id: int):
    return await Post.like(post_id=post_id, session=session)


@app.post('/post/', response_model=Post)
async def create_post(post: PostBase):
    return await post.create(session=session)


if __name__ == '__main__':
    uvicorn.run('main:app', host='localhost', port=8282, reload=True)
