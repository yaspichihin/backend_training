from fastapi import APIRouter
from fastapi_cache.decorator import cache
from datetime import date, time

from app.hotels.dao import HotelsDAO

from app.hotels.schemas import SHotels, SHotelsRoomsLeft

import asyncio

router = APIRouter(
    prefix = "/hotels",
    tags = ["Hotels"]
)

# Вернуть все отели
@router.get("/all")
@cache(expire=10)
async def get_all_hotels(
) -> list[SHotels]:
    return await HotelsDAO.select_all_filter()

# Вернуть отель по его id
@router.get("/id")
@cache(expire=10)
async def get_hotel_by_id(
    hotel_id: str,
) -> SHotels:
    return await HotelsDAO.select_one_or_none_filter_by(
        id = int(hotel_id))

# Вернуть отели по совпадению слова из location и наличии свободных номеров
@router.get("/{location}")
@cache(expire=10)
async def get_hotels_by_location(
    location: str,
    date_from: date,
    date_to: date,
) -> list[SHotelsRoomsLeft]:
    # await asyncio.sleep(3)
    return await HotelsDAO.find_hotels_by_location(
        location, date_from, date_to)