from fastapi import HTTPException, status
from pydantic import HttpUrl
from sqlmodel import Field, SQLModel, Relationship

from database import SessionMixin


class PostBase(SessionMixin, SQLModel):
    content: str = Field(...)
    image: HttpUrl = Field(...)

    class Config:
        schema_extra = {'example': {
            'content': 'here some content',
            'image': 'https://picsum.photos/id/237/200/300'
        }}


class PostCreate(PostBase):

    async def create(self, user_id):
        with self._session:
            post = Post.from_orm(self)
            post.user_id = user_id
            self._session.add(post)
            self._session.commit()
            self._session.refresh(post)
            return post


class PostUpdate(SQLModel):
    content: str | None = None
    image: HttpUrl | None = None

    class Config:
        schema_extra = {'example': {
            'content': 'here some content',
            'image': 'https://picsum.photos/id/237/200/300'
        }}
        orm_mode = True


class Post(PostBase, table=True):
    __tablename__ = 'post'
    id: int = Field(default=None, primary_key=True)
    likes: int = Field(default=0, index=True)
    user_id: int | None = Field(foreign_key='user.id')
    owner: "User" = Relationship(back_populates='posts')

    @classmethod
    async def get(cls, post_id: int, user_id: int):
        exception = HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Permissions denied',
            headers={'WWW-Authenticate': 'Bearer'}

        )
        with cls._session:
            post = cls._session.get(cls, post_id)
            if not post:
                raise HTTPException(status_code=404, detail='Post does not exist')
            if not post.owner.id == user_id:
                raise exception
            return post

    @classmethod
    async def like(cls, post_id: int):
        with cls._session:
            post = cls._session.get(cls, post_id)
            post.likes += 1
            cls._session.commit()
            cls._session.refresh(post)
            if not post:
                raise HTTPException(status_code=404, detail='Post does not exist')
            return post

    @classmethod
    async def unlike(cls, post_id: int):
        with cls._session:
            post = cls._session.get(cls, post_id)
            if post.likes > 0:
                post.likes -= 1
                if not post:
                    raise HTTPException(status_code=404, detail='Post does not exist')
            return post

    async def update(self, post_data: dict, user_id: int):
        exception = HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Permissions denied',
            headers={'WWW-Authenticate': 'Bearer'}

        )
        if not self.owner.id == user_id:
            raise exception
        with self._session:
            for key, value in post_data.items():
                setattr(self, key, value)
            self._session.add(self)
            self._session.commit()
            self._session.refresh(self)
            return self

    @classmethod
    async def delete(cls, post_id: int, user_id: int):
        post = await Post.get(post_id, user_id=user_id)
        cls._session.delete(post)
        cls._session.commit()


class PostRead(Post, table=False):
    pass


# TODO https://sqlmodel.tiangolo.com/tutorial/fastapi/relationships/#models-with-relationships

from models.user import User

User.update_forward_refs()
# FIX circular import
# https://stackoverflow.com/questions/63420889/fastapi-pydantic-circular-references-in-separate-files

if __name__ == "__main__":
    pass
