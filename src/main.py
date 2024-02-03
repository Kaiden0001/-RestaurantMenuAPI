from contextlib import asynccontextmanager
from typing import AsyncGenerator

from aioredis import from_url
from fastapi import FastAPI

from src.database import REDIS_URL
from src.menu.api.dish_api import router as router_dish
from src.menu.api.menu_api import router as router_menu
from src.menu.api.submenu_api import router as router_submenu


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    async with await from_url(REDIS_URL) as redis:
        await redis.flushdb(asynchronous=True)

    yield


app: FastAPI = FastAPI(lifespan=lifespan)

app.include_router(router_menu)
app.include_router(router_submenu)
app.include_router(router_dish)
