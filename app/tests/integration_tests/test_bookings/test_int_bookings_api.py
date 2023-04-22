import warnings
from httpx import AsyncClient
import pytest


# Прописали params чтобы обойти pydantic
@pytest.mark.parametrize("room_id,date_from,date_to,booked_rooms,status_code", [
    # 2 брони уже в БД + создадим новых 8 всего номеров 10
    (4, "2030-05-01", "2030-05-15", 3, 200),
    (4, "2030-05-01", "2030-05-15", 4, 200),
    (4, "2030-05-01", "2030-05-15", 5, 200),
    (4, "2030-05-01", "2030-05-15", 6, 200),
    (4, "2030-05-01", "2030-05-15", 7, 200),
    (4, "2030-05-01", "2030-05-15", 8, 200),
    (4, "2030-05-01", "2030-05-15", 9, 200),
    (4, "2030-05-01", "2030-05-15", 10, 200),
    # Новые брони не создаются когда номера закончились
    (4, "2030-05-01", "2030-05-15", 10, 409),
    (4, "2030-05-01", "2030-05-15", 10, 409),
    # Дата заезда >= Дата выезда (неверные параметры)
    (4, "2025-05-01", "2025-04-15", 10, 409),
    # Дата выезда - Дата заезда > 30 дней (неверные параметры)
    (4, "2025-05-01", "2025-07-15", 10, 409),
])
async def test_add_and_get_booking(
    room_id,
    date_from,
    date_to,
    booked_rooms,
    status_code,
    async_auth_client: AsyncClient
):
    response = await async_auth_client.post("/bookings", params={
        "room_id": room_id,
        "date_from": str(date_from),
        "date_to": str(date_to)
    })
    assert response.status_code == status_code

    # Проверка кол-ва забронированных номеров
    response = await async_auth_client.get("/bookings")
    assert len(response.json()) == booked_rooms

async def test_get_and_delete_all_bookings(async_auth_client: AsyncClient):
    response = await async_auth_client.get("/bookings")
    # В наличии должно быть 10 брони, 2 было и 8 добавили на предыдушем шаге
    assert len(response.json()) == 10
    # Проверим удаление записей
    for booking in response.json():
        response = await async_auth_client.delete(f"/bookings/{booking['id']}")
        assert response.status_code == 204
    response = await async_auth_client.get("/bookings")
    assert len(response.json()) == 0
    


