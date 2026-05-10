from dotenv import load_dotenv
load_dotenv()
from contextlib import asynccontextmanager
from starlette.responses import FileResponse
from orm import AsyncORM
from fastapi import FastAPI
from database import session_factory
from routers import auth, account, deposit, client


@asynccontextmanager
async def lifespan(app: FastAPI):
    await AsyncORM.create_tables()
    await AsyncORM.insert_data()
    async with session_factory() as session:
        await AsyncORM.insert_admin_data(session)
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(auth.router)
app.include_router(client.router)
app.include_router(deposit.router)
app.include_router(account.router)