import os
from sqlmodel import create_engine, Session, SQLModel

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

engine = create_engine(f'sqlite:///{ROOT_DIR}/api.db')

session = Session(engine)


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
