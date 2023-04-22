from datetime import date

from fastapi import APIRouter, BackgroundTasks, Depends, Response
from pydantic import parse_obj_as

from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBooking, SBookingWithRoomInfo
from app.tasks.tasks import send_booking_confirmation_email
from app.users.dependencies import get_current_user
from app.users.models import Users

router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"],  # Для объединения в одну группу
)


# Вернуть все забронированные номера пользователем
@router.get("")
async def get_booking(
    user: Users = Depends(get_current_user),
) -> list[SBookingWithRoomInfo]:
    return await BookingDAO.get_booking_for_user(user)


# Для бронирования номеров по пользователю
@router.post("")
async def add_booking(
    background_tasks: BackgroundTasks,
    room_id: int,
    date_from: date,
    date_to: date,
    user: Users = Depends(get_current_user),
) -> SBooking:
    booking = await BookingDAO.add_booking_for_user(
        user.id, room_id, date_from, date_to
    )
    booking_dict = parse_obj_as(SBooking, booking).dict()
    # Вариант с Celery, не забыть включить декоратор в таске
    # send_booking_confirmation_email.delay(booking_dict, user.email)
    # Вариант со встроенным BackgroundTasks не забыть выключить декоратор в таске
    background_tasks.add_task(send_booking_confirmation_email, booking_dict, user.email)
    return booking_dict


@router.delete("/{booking_id}")
async def delete_booking(
    response: Response,
    booking_id: int,
    user: Users = Depends(get_current_user),
) -> None:
    await BookingDAO.delete_booking_for_user(
        booking_id=int(booking_id), user_id=user.id
    )
    response.status_code = 204


# @router.get("/check_request")
# async def check_request(request: Request):
#     print(request.cookies)
#     print(request.url)
#     print(request.client)
