import os

from sqlmodel import create_engine, Session, SQLModel
from settings import settings

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

engine = create_engine(settings.db_path)

session = Session(engine)


async def create_db_and_tables(connection):
    SQLModel.metadata.create_all(connection)


if __name__ == '__main__':
    import time
    from main import logger

    SQLModel.metadata.drop_all(engine)
    time.sleep(1)
    logger.info(msg='DROPPED')
    # SQLModel.metadata.create_all(engine)
    # time.sleep(1)
    # logger.info(msg='CREATED')
