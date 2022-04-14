from sqlmodel import create_engine, Session, SQLModel

from settings import settings

engine = create_engine(settings.db_path, connect_args={'check_same_thread': False})


class SessionMixin(SQLModel):
    _session: Session = Session(engine)


if __name__ == '__main__':
    import time
    import logging
    import os
    from models import User, Post

    logging.basicConfig(level=10)
    logger = logging.getLogger(name='database')

    if not os.path.exists('instafood_db'):
        try:
            SQLModel.metadata.create_all(engine)
            time.sleep(1)
            logger.info(msg='CREATED')
        except Exception as e:
            logger.info(msg=e)
    else:
        logger.info(msg='DATABASE EXISTS')
