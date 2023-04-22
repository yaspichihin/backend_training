from datetime import datetime

from app.bookings.dao import BookingDAO


data = {
    "user_id": 2,
    "room_id": 2,
    "date_from": datetime.strptime("2023-07-01", "%Y-%m-%d"),
    "date_to": datetime.strptime("2023-07-15", "%Y-%m-%d"),
}

# Провеока добавлиния бронирования
async def test_crud_booking():
    new_booking = await BookingDAO.add_booking_for_user(
        user_id=data["user_id"],
        room_id=data["room_id"],
        date_from=data["date_from"],
        date_to=data["date_to"],
    )
    assert new_booking.user_id == data["user_id"]
    assert new_booking.room_id == data["room_id"]
    assert await BookingDAO.select_one_or_none_filter_by(id=new_booking.id)
    assert await BookingDAO.get_booked_rooms(
        data["room_id"], data["date_from"], data["date_to"]
    )
    await BookingDAO.delete_booking_for_user(new_booking.id, data["user_id"])
    assert await BookingDAO.select_one_or_none_filter_by(id=new_booking.id) is None
