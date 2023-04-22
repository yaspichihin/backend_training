from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from sqladmin import Admin

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
from app.users.router import router_auth as router_user

app = FastAPI()

# Роутер для api
app.include_router(router_auth)
app.include_router(router_user)
app.include_router(router_bookings)
app.include_router(router_hotels)
app.include_router(router_rooms)


# Роутер для frontend
app.include_router(router_pages)

# Добавление картинок
app.mount("/static", StaticFiles(directory="app/static"), "static")
app.include_router(router_images)


# Добавим площадки с которых к нам хотят обращаться
origins = [
    # "http://localhost:3000",
    # "http://localhost:6379",
    # "http://192.168.1.60:6379",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=[
        "Content-Type",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Access-Authorization",
    ],
)


# Добавление Redis для кэширования частых запросов
# Данный декоратор прогоняет код перед запуском FastAPI
@app.on_event("startup")
async def startup():
    redis = await aioredis.from_url(
        settings.redis_url, encoding="utf8", decode_responses=True
    )
    FastAPICache.init(RedisBackend(redis), prefix="fastapi")


# Данный декоратор прогоняет код после завершения программы
@app.on_event("shutdown")
def shutdown_event():
    pass


# Настрока Админки
admin = Admin(app, engine, authentication_backend=authentication_backend)
admin.add_view(UsersAdmin)
admin.add_view(BookingsAdmin)
admin.add_view(HotelsAdmin)
admin.add_view(RoomsAdmin)
