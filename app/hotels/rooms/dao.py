from datetime import date

from app.bookings.dao import BookingDAO
from app.dao.base import BaseDAO
from app.hotels.rooms.models import Rooms
from app.hotels.rooms.schemas import SRooms, SRoomsRoomLeft


class RoomsDAO(BaseDAO):
    model = Rooms

    @classmethod
    async def get_available_rooms_by_hotel_id(
        cls,
        hotel_id: int,
        date_from: date,
        date_to: date,
    ) -> list[SRoomsRoomLeft]:
        # Создадим список для формирования ответа
        result: list = []
        # Получим все комнаты по hotel_id
        rooms: list[SRooms] = [room for room in
                await cls.select_all_filter(Rooms.hotel_id == hotel_id)]
        # Подсчитаем доступное количество комнат
        for room in rooms:
                rooms_qty = room.quantity
                rooms_booked = len(await BookingDAO.get_booked_rooms(
                     room.id, date_from, date_to))
                rooms_left: int = rooms_qty - rooms_booked
                if rooms_left:
                    room.rooms_left = rooms_left
                    result.append(room)
        return result
                        