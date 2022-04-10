import logging

import uvicorn
from fastapi import FastAPI, Form, UploadFile, File

from api import router
from database import create_db_and_tables
from database import session, engine
from settings import settings

logging.basicConfig(level=10)

logger = logging.getLogger(name='DB LOGGER')
app = FastAPI()
app.include_router(router=router)


@app.on_event('startup')
async def on_startup():
    logger.info(msg='CREATING DB')
    await create_db_and_tables(connection=engine)


@app.on_event('shutdown')
async def on_shutdown():
    session.close()
    logger.info(msg='DB CONNECTION CLOSED')


@app.post("/files/")
async def create_file(file: bytes = File(...)):
    return {"file_size": len(file)}  # !TODO files uploads


@app.post("/uploadfile/")
async def create_upload_file(file: list[UploadFile]):
    return {"filename": file}  # !TODO files uploads


@app.post("/login/")
async def login(username: str = Form(...), password: str = Form(...)):
    return {"username": username}


if __name__ == '__main__':
    uvicorn.run('main:app', host=settings.server_host, port=settings.server_port, reload=True)
