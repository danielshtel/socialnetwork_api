from fastapi import HTTPException
from pydantic import HttpUrl
from sqlmodel import Field, SQLModel, Session


class PostBase(SQLModel):
    content: str = Field(...)
    image: HttpUrl = Field(...)

    class Config:
        schema_extra = {'example': {
            'content': 'here some content',
            'image': 'https://picsum.photos/id/237/200/300'
        }}

    async def create(self, session: Session):
        with session:
            post = Post.from_orm(self)
            session.add(post)
            session.commit()
            session.refresh(post)
            return post


class PostUpdate(SQLModel):
    content: str | None = None
    image: HttpUrl | None = None

    class Config:
        schema_extra = {'example': {
            'content': 'here some content',
            'image': 'https://picsum.photos/id/237/200/300'
        }}


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

    async def update(self, post_data: dict, session: Session):
        for key, value in post_data.items():
            setattr(self, key, value)
        session.add(self)
        session.commit()
        session.refresh(self)
        return self
