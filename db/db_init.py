from sqlmodel import SQLModel
from db.config import engine


async def create_db_and_tables(connection):
    SQLModel.metadata.create_all(connection)


if __name__ == '__main__':
    from models.user import User
    from models.post import Post
    import time
    from main import logger

    SQLModel.metadata.drop_all(engine)
    time.sleep(1)
    logger.info(msg='DROPPED')
    SQLModel.metadata.create_all(engine)
    time.sleep(1)
    logger.info(msg='CREATED')
