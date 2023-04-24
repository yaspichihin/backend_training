import time
import sentry_sdk
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from sqladmin import Admin
from fastapi_versioning import VersionedFastAPI, version
from prometheus_fastapi_instrumentator import Instrumentator

from app.admin.auth import authentication_backend
from app.admin.views import BookingsAdmin, HotelsAdmin, RoomsAdmin, UsersAdmin
from app.bookings.router import router as router_bookings
from app.config import settings
from app.db import engine
from app.hotels.rooms.router import router as router_rooms
from app.hotels.router import router as router_hotels
from app.images.router import router as router_images
from app.pages.router import router as router_pages
from app.users.router import router_auth as router_auth
from app.users.router import router_user as router_user
from app.logger import logger


app = FastAPI(
    title="Бронирование Отелей",
    version="0.1.0",
    root_path="/api",
)


sentry_sdk.init(
    dsn=settings.sentry_dsn,
    traces_sample_rate=1.0,
)


# Роутер для api
app.include_router(router_auth)
app.include_router(router_user)
app.include_router(router_bookings)
app.include_router(router_hotels)
app.include_router(router_rooms)

# Роутер для frontend
app.include_router(router_pages)


# Добавим площадки с которых к нам хотят обращаться
origins = [
    "http://localhost:3000",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", 
                   "Access-Control-Allow-Origin",
                   "Authorization"],
)


app = VersionedFastAPI(app,
    version_format="{major}",
    prefix_format="/v{major}",
)


if settings.mode == "test":
    redis = aioredis.from_url(
        settings.redis_url, encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="cache")

# Добавление Redis для кэширования частых запросов
# Данный декоратор прогоняет код перед запуском FastAPI
@app.on_event("startup")
async def startup():
    redis = await aioredis.from_url(
        settings.redis_url, encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi")


# Добавим экспортер для prometeus
instrumentator = Instrumentator(
    should_group_status_codes=False,
    excluded_handlers=[".*admin.*", "/metrics"],
)
instrumentator.instrument(app).expose(app)

# Позволяет работать с request и respose
# Брать и добавлять данные
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    # При подключении Prometheus + Grafana подобный лог не требуется
    # logger.info("Request handling time", extra={
    #     "process_time": round(process_time, 4)
    # })
    return response

# Добавление картинок
app.mount("/static", StaticFiles(directory="app/static"), "static")
app.include_router(router_images)


# Настрока Админки
admin = Admin(app, engine, authentication_backend=authentication_backend)
admin.add_view(UsersAdmin)
admin.add_view(BookingsAdmin)
admin.add_view(HotelsAdmin)
admin.add_view(RoomsAdmin)
