from fastapi import APIRouter, status, Response, Depends

from models import Post, PostUpdate, PostCreate, PostRead, User
from utils import get_current_user

router = APIRouter(prefix='/post', tags=['post'])


@router.get('/{post_id}',
            response_model=PostRead)  # TODO https://sqlmodel.tiangolo.com/tutorial/fastapi/relationships/#models-with-relationships
async def get_post(post_id: int, user: User = Depends(get_current_user)):
    return await Post.get(post_id=post_id, user_id=user.id)


@router.get('/like/{post_id}', response_model=Post, response_model_exclude={'id'})
async def like_post(post_id: int):
    return await Post.like(post_id=post_id)


@router.post('/{user_id}', response_model=Post)
async def create_post(post: PostCreate, user: User = Depends(get_current_user)):
    return await post.create(user_id=user.id)


@router.patch('/', response_model=Post)
async def update_post(post_id: int, post_data: PostUpdate, user: User = Depends(get_current_user)):
    post = await Post.get(post_id=post_id, user_id=user.id)
    data = post_data.dict(exclude_unset=True)
    return await post.update(post_data=data, user_id=user.id)


@router.delete('/', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int, user: User = Depends(get_current_user)):
    await Post.delete(post_id=post_id, user_id=user.id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
