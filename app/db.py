from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import settings

# Составим ссылку для подключения, требует SQLAlchemy
if settings.mode == "test":
    databse_url = settings.databse_test_url
    databse_params = {"poolclass": NullPool}
else:
    databse_url = settings.databse_url
    databse_params = {}

# Создаем движок для подключения
engine = create_async_engine(databse_url, **databse_params)

# Создадим фабрику(Генератор сессий/транзакций)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


# Класс для миграций, тут будут собираться данные от всех моделей,
# которые будут наследоваться от этого класса, чтобы alembic мог сравнить
# наше состояние на backend и в BD. Если состоение в BD не соответсвует
# как на Backend, то начинает выполнять миграции для приведения актуального состояния.
class Base(DeclarativeBase):
    pass
