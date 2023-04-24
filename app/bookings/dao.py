from datetime import date, timedelta

from sqlalchemy import and_, select
from sqlalchemy.exc import SQLAlchemyError

from app.bookings.models import Bookings
from app.bookings.schemas import SBooking, SBookingWithRoomInfo
from app.dao.base import BaseDAO
from app.db import async_session_maker
from app.exceptions import (
    BookingDoesNotExistException,
    DateFromMoreOrEqualDateToException,
    LongBookingException,
    RoomCannotBeBookedException,
)
from app.hotels.rooms.models import Rooms
from app.users.models import Users
from app.logger import logger

class BookingDAO(BaseDAO):
    model = Bookings

    @classmethod
    async def get_booked_rooms(cls, room_id: int, date_from: date, date_to: date) -> int:
        # Проверка заданных дат
        if date_from >= date_to:
            raise DateFromMoreOrEqualDateToException
        # Вернуть количество забронированных комнат
        return await cls.select_all_filter(
            and_(
                Bookings.room_id == room_id,
                and_(Bookings.date_to >= date_from, Bookings.date_from <= date_to),
            )
        )

    @classmethod
    async def get_booking_for_user(cls, user: Users) -> list[SBookingWithRoomInfo]:
        async with async_session_maker() as session:
            query = (
                select(
                    Bookings.id,
                    Bookings.room_id,
                    Bookings.user_id,
                    Bookings.date_from,
                    Bookings.date_to,
                    Bookings.price,
                    Bookings.total_cost,
                    Bookings.total_days,
                    Rooms.image_id,
                    Rooms.name,
                    Rooms.description,
                    Rooms.services,
                )
                .select_from(Bookings)
                .join(Rooms, Bookings.room_id == Rooms.id, isouter=True)
                .where(Bookings.user_id == user.id)
            )

            result = await session.execute(query)
            return result.all()

    @classmethod
    async def add_booking_for_user(cls, user_id: int, room_id: int,
        date_from: date, date_to: date) -> SBooking:
        try:
            # Дата выезда - Дата заезда > 30 дней (неверные параметры)
            if date_from + timedelta(days=30) < date_to:
                raise LongBookingException
            booked_rooms: int = len(await cls.get_booked_rooms(room_id, date_from, date_to))
            async with async_session_maker() as session:
                total_rooms: int = (await session.execute(
                    select(Rooms.quantity).filter_by(id=room_id))).scalar()
                # Если комнат для бронирования нет выводи ошибку
                if not total_rooms - booked_rooms:
                    raise RoomCannotBeBookedException
                # Получаем стоимость комнаты за 1 день
                price: int = (await session.execute(
                    select(Rooms.price).filter_by(id=room_id))).scalar()
                # Добавим бронь
                return (await cls.add_rows(room_id=room_id,user_id=user_id,
                    date_from=date_from,date_to=date_to,price=price)).scalar()
        # Добавление логгирования
        except (SQLAlchemyError, Exception) as err:
            if isinstance(err, SQLAlchemyError):
                msg: str = "DB"
            elif isinstance(err, Exception):
                msg: str = "Unknown"
            msg += "Exception: Cannot add booking"
            extra = {
                "user_id": user_id,
                "room_id": room_id, 
                "date_from": date_from, 
                "date_to": date_to,
            }
            logger.error(msg, extra=extra, exc_info=True)

    @classmethod
    async def delete_booking_for_user(cls, booking_id: int, user_id: int) -> None:
        # Проверка наличия брони пользователем
        if not await cls.select_one_or_none_filter_by(id=booking_id, user_id=user_id):
            raise BookingDoesNotExistException
        # Удаляем бронь
        await cls.delete_rows_filer_by(id=booking_id, user_id=user_id)
