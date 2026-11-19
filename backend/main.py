from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from starlette.responses import FileResponse

from backend.core.config import settings
from backend.core.exceptions import register_exception_handlers
from backend.core.models import db_helper
from backend.routers import router as api_router
from backend.services import SeedService


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    async with db_helper.session_factory() as session:
        await SeedService(session).run()
    yield
    # shutdown
    await db_helper.dispose()


app = FastAPI(lifespan=lifespan)
register_exception_handlers(app)
app.include_router(api_router)


@app.get("/")
async def root():
    return FileResponse("index.html")


if __name__ == "__main__":
    uvicorn.run(
        "backend.main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
