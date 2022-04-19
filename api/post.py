from fastapi import APIRouter, status, Response

from models import Post, PostUpdate, PostCreate, PostRead

router = APIRouter(prefix='/post')


@router.get('/{post_id}', response_model=PostRead, tags=[
    'post'])  # TODO https://sqlmodel.tiangolo.com/tutorial/fastapi/relationships/#models-with-relationships
async def get_post(post_id: int):
    return await Post.get(post_id=post_id)


@router.get('/like/{post_id}', response_model=Post, response_model_exclude={'id'}, tags=['post'])
async def like_post(post_id: int):
    return await Post.like(post_id=post_id)


@router.post('/{user_id}', response_model=Post, tags=['post'])
async def create_post(user_id: int, post: PostCreate):
    return await post.create(user_id=user_id)


@router.patch('/', response_model=Post, tags=['post'])
async def update_post(post_id: int, post_data: PostUpdate):
    post = await Post.get(post_id=post_id)
    data = post_data.dict(exclude_unset=True)
    return await post.update(post_data=data)


@router.delete('/', status_code=status.HTTP_204_NO_CONTENT, tags=['post'])
async def delete_post(post_id: int):
    await Post.delete(post_id=post_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
