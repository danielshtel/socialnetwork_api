from fastapi import HTTPException
from sqlmodel import Field, SQLModel, Session


class PostBase(SQLModel):
    content: str = Field(default=None)

    async def create(self, session: Session):
        with session:
            post = Post.from_orm(self)
            session.add(post)
            session.commit()
            session.refresh(post)
            return post


class PostResponseView(SQLModel):
    content: str
    likes: int


class Post(PostBase, table=True):
    __tablename__ = 'post'
    id: int = Field(default=None, primary_key=True)
    likes: int = Field(default=0, index=True)

    @classmethod
    async def get(cls, session: Session, post_id: int):
        post = session.get(cls, post_id)
        if not post:
            raise HTTPException(status_code=404, detail='Post does not exist')
        return post

    @classmethod
    async def like(cls, session: Session, post_id: int):

        post = session.get(cls, post_id)
        post.likes += 1
        session.commit()
        if not post:
            raise HTTPException(status_code=404, detail='Post does not exist')
        return post

    @classmethod
    async def unlike(cls, session: Session, post_id: int):
        post = session.get(cls, post_id)
        if post.likes > 0:
            post.likes -= 1
            if not post:
                raise HTTPException(status_code=404, detail='Post does not exist')
        return post
