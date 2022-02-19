from typing import Optional

from fastapi import HTTPException
from pydantic import EmailStr
from sqlmodel import Field, SQLModel, Session, create_engine, select


class UserBase(SQLModel):
    name: str = Field(default=None, index=True)
    email: EmailStr = Field(default=None, index=True)
    age: int = Field(default=None, index=True)

    async def create(self, session: Session):
        with session:
            user = User.from_orm(self)
            session.add(user)
            session.commit()
            session.refresh(user)
            return user


class User(UserBase, table=True):
    __tablename__ = 'user'

    id: int = Field(default=None, primary_key=True)

    class Config:
        orm_mode = True

    @classmethod
    async def get_all(cls, session: Session, limit: int, offset: int = 0) -> list:
        return session.exec(select(cls).offset(offset).limit(limit)).all()

    @classmethod
    async def get_user(cls, session: Session, u_id: int):
        user = session.get(cls, u_id)
        if not user:
            raise HTTPException(status_code=404, detail='User does not exist')
        return user

    async def update_user(self):
        pass  # !TODO refactor sessions && update

    async def delete_user(self, session: Session):
        session.delete(self)
        session.commit()
        return {'ok': True}


class UserUpdate(SQLModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    age: Optional[int] = None


async def create_db_and_tables(connection):
    SQLModel.metadata.create_all(connection)


if __name__ == '__main__':
    from pathlib import Path
    from time import sleep

    SOURCE_DIR = Path(__file__).resolve().parent.parent

    connect_args = {"check_same_thread": False}
    engine = create_engine(f'sqlite:///{SOURCE_DIR}/api.db', connect_args=connect_args)
    SQLModel.metadata.drop_all(engine)
    sleep(1)
    SQLModel.metadata.create_all(engine)
    sleep(1)
