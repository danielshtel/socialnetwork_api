from sqlmodel import SQLModel


async def create_db_and_tables(connection):
    SQLModel.metadata.create_all(connection)
