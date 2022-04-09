import os

from sqlmodel import create_engine, Session

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

engine = create_engine(f'sqlite:///{ROOT_DIR}/api.db')

session = Session(engine)

if __name__ == '__main__':
    pass
