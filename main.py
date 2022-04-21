import logging

import uvicorn
from fastapi import FastAPI
from sqlmodel import Session

from api import router
from database import engine, db_init
from settings import settings

logging.basicConfig(level=10)

logger = logging.getLogger(name=__name__)
app = FastAPI()
app.include_router(router=router)


@app.on_event('startup')
async def on_startup():
    db_init()
    logger.info('Interactive docs: http://0.0.0.0:8000/docs')


@app.on_event('shutdown')
async def on_shutdown():
    session = Session(engine)
    session.close()
    logger.info(msg='DB CONNECTION CLOSED')


# @app.post("/files/")
# async def create_file(file: bytes = File(...)):
#     return {"file_size": len(file)}  # !TODO files uploads
#
#
# @app.post("/uploadfile/")
# async def create_upload_file(file: list[UploadFile]):
#     return {"filename": file}  # !TODO files uploads
#
#
# @app.post("/login/")
# async def login(username: str = Form(...), password: str = Form(...)):
#     return {"username": username}


if __name__ == '__main__':
    uvicorn.run('main:app', host=settings.server_host, port=settings.server_port, reload=True)

# TODO user routes
# TODO hide password
# TODO custom age validators or something like that
# TODO read more about dependencies FastAPI
# TODO upload static images
