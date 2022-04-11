from sqlalchemy.orm import declarative_base
from sqlmodel import create_engine, Session, SQLModel

from settings import settings

engine = create_engine(settings.db_path, connect_args={'check_same_thread': False})
Base = declarative_base()


class SessionMixin(SQLModel):
    _session: Session = Session(engine)


if __name__ == '__main__':
    import time
    import logging

    logging.basicConfig(level=10)
    logger = logging.getLogger(name='database')

    SQLModel.metadata.drop_all(engine)
    time.sleep(1)
    logger.info(msg='DROPPED')
    SQLModel.metadata.create_all(engine)
    time.sleep(1)
    logger.info(msg='CREATED')
