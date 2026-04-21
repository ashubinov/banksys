from fastapi import Depends
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from typing import Annotated

DATABASE_URL = "postgresql+psycopg://postgres:admin@127.0.0.1:5432/postgres"

engine = create_async_engine(DATABASE_URL)

session_factory = async_sessionmaker(engine, expire_on_commit=False)

async def get_session():
    async with session_factory() as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_session)]

class Base(DeclarativeBase):
    pass