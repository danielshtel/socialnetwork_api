import os
from typing import Optional
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

    id: Optional[int] = Field(default=None, primary_key=True)

    class Config:
        orm_mode = True

    @classmethod
    async def get_list(cls, session: Session):
        return session.exec(select(cls)).all()


async def create_db_and_tables(connection):
    SQLModel.metadata.create_all(connection)


if __name__ == '__main__':
    from time import sleep

    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

    connect_args = {"check_same_thread": False}
    engine = create_engine(f'sqlite:///{ROOT_DIR}/api.db', connect_args=connect_args)
    SQLModel.metadata.drop_all(engine)
    sleep(1)
    SQLModel.metadata.create_all(engine)
    sleep(1)
