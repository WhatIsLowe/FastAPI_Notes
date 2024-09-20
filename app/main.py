from fastapi import FastAPI

from backend.database.database import engine_pg
from backend.database.models import Base

from backend.api.routers.auth import router as auth_router

app = FastAPI()


@app.on_event("startup")
async def create_tables():
    async with engine_pg.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app.include_router(auth_router)
