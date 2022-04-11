from fastapi import APIRouter


from models import Post, PostBase, PostUpdate

router = APIRouter(prefix='/post')


@router.get('/{post_id}', response_model=Post, tags=['post'])
async def get_post(post_id: int):
    return await Post.get(post_id=post_id)


@router.get('/like/{post_id}', response_model=Post, response_model_exclude={'id'}, tags=['post'])
async def like_post(post_id: int):
    return await Post.like(post_id=post_id)


@router.post('/', response_model=Post, tags=['post'])
async def create_post(post: PostBase):
    return await post.create()


@router.patch('/', response_model=Post, tags=['post'])
async def update_post(post_id: int, post_data: PostUpdate):
    post = await Post.get(post_id=post_id)
    data = post_data.dict(exclude_unset=True)
    return await post.update(post_data=data)
