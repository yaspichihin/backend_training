from datetime import date

from sqlalchemy import func

from app.bookings.dao import BookingDAO
from app.dao.base import BaseDAO
from app.hotels.models import Hotels
from app.hotels.rooms.dao import RoomsDAO
from app.hotels.rooms.models import Rooms
from app.hotels.schemas import SHotelsRoomsLeft


class HotelsDAO(BaseDAO):
    model = Hotels
    
    @classmethod
    async def find_hotels_by_location(
          cls,
          location: str,
          date_from: date,
          date_to: date,
    ) -> list[SHotelsRoomsLeft]:
        # Создадим список для формирования ответа
        result: list = []
        # Получить все отели по location
        hotels = await cls.select_all_filter(
             func.lower(Hotels.location).like(f"%{location.lower()}%"))
        
        # Выполнить проверку по наличии свободных комнат для каждого отеля
        for hotel in hotels:
              # Получим сколько всего комнат в отеле
              total_rooms: int = hotel.rooms_quantity
              # Получим список room_id комнат отеля
              rooms: list[int] = [room.id for room in 
                  await RoomsDAO.select_all_filter(Rooms.hotel_id == hotel.id)]
              
              # Получим сколько забронировано комнат для данного отеля по указаным датам
              qty_booked_rooms: int = 0
              for room_id in rooms:
                    qty_booked_rooms += len(await BookingDAO.get_booked_rooms(
                         room_id, date_from, date_to))
                    
              if total_rooms > qty_booked_rooms:
                    hotel.rooms_left = total_rooms - qty_booked_rooms
                    result.append(hotel)
                    
        return result