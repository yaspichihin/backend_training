from datetime import date

from fastapi import APIRouter

from app.hotels.rooms.dao import RoomsDAO
from app.hotels.rooms.schemas import SRoomsRoomLeft

router = APIRouter(prefix="/hotels", tags=["Rooms"])


# Вернуть все номера отеля по его hotel_id
@router.get("/{hotel_id}/rooms")
async def get_all_rooms_by_hotel_id(
    hotel_id: str, data_from: date, data_to: date
) -> list[SRoomsRoomLeft]:
    return await RoomsDAO.get_available_rooms_by_hotel_id(
        int(hotel_id), data_from, data_to
    )
