import os
from sqlmodel import create_engine, Session, SQLModel

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

engine = create_engine(f'sqlite:///{ROOT_DIR}/api.db')

session = Session(engine)


if __name__ == '__main__':
    from models.user import User
    from models.post import Post
    SQLModel.metadata.drop_all(engine)