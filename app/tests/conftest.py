import asyncio
from datetime import datetime
import pytest
from sqlalchemy import insert
import json

from app.config import settings
from app.db import Base, async_session_maker, engine

from app.bookings.models import Bookings
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.users.models import Users

from httpx import AsyncClient
from app.main import app as fastapi_app


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    # Проверим, что находимся в режиме тестирования
    assert settings.mode == "test"

    # Создание тестовых таблиц без alembic
    async with engine.begin() as conn:
        # Удалить таблицы
        await conn.run_sync(Base.metadata.drop_all)
        # Создать пустые таблицы
        await conn.run_sync(Base.metadata.create_all)

    def open_mock_json(model: str):
        with open(f"app/tests/mock_{model}.json", encoding="utf-8") as file:
            return json.load(file)
        
    hotels = open_mock_json("hotels")
    rooms = open_mock_json("rooms")
    users = open_mock_json("users")
    bookings = open_mock_json("bookings")

    for booking in bookings:
        booking["date_from"] = datetime.strptime(booking["date_from"], "%Y-%m-%d")
        booking["date_to"] = datetime.strptime(booking["date_to"], "%Y-%m-%d")

    async with async_session_maker() as session:
        add_hotels = insert(Hotels).values(hotels)
        add_rooms = insert(Rooms).values(rooms)
        add_users = insert(Users).values(users)             # Добавлять перед Bookings из-за связей
        add_bookings = insert(Bookings).values(bookings)

        await session.execute(add_hotels)
        await session.execute(add_rooms)
        await session.execute(add_users)
        await session.execute(add_bookings)

        await session.commit()


# Взято из документации к pytest-asyncio
@pytest.fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

# function - чистый клиент без cookies

# Создадим чистый клиент
@pytest.fixture(scope="function")
async def async_client():
    async with AsyncClient(app=fastapi_app, base_url="http://test") as async_client:
        yield async_client


# Фикстура для сессии БД тут не потребуется, полезно знать
@pytest.fixture(scope="function")
async def session():
    async with async_session_maker() as session:
        yield session

# session - 1 раз залогинить на сессию
# Фикстура залогиненного пользователя
@pytest.fixture(scope="session")
async def async_auth_client():
    async with AsyncClient(app=fastapi_app, base_url="http://test") as async_auth_client:
        # Залогинем пользователя
        await async_auth_client.post("/auth/login", json={
            "email": "test@test.com",
            "password": "test"
        })
        # Проверим наличие jwt токена
        assert async_auth_client.cookies["booking_access_token"]
        yield async_auth_client
