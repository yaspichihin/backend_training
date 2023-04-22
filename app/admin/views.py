from sqladmin import ModelView

from app.users.models import Users
from app.bookings.models import Bookings
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms


class UsersAdmin(ModelView, model=Users):
    column_list = [Users.id, Users.email]                   # Какие столбцы будут отображаться
    column_details_exclude_list = [Users.hashed_password]   # Исключить данные из детального просмотра
    can_delete = False      # Запрет на удаление строк
    name = "User"           # Имя строки
    name_plural = "Users"   # Имя таблицы
    icon = "fa-solid fa-user"

class BookingsAdmin(ModelView, model=Bookings):
    column_list = [c.name for c in Bookings.__table__.c]    # Взять из модели все названия колонок
    column_list += [Bookings.user, Bookings.room]
    name = "Booking"           # Имя строки
    name_plural = "Bookings"   # Имя таблицы
    icon = "fa-solid fa-calendar"

class HotelsAdmin(ModelView, model=Hotels):
    column_list = [c.name for c in Hotels.__table__.c] 
    column_list += [Hotels.rooms]
    name = "Hotel"
    name_plural = "Hotels"
    icon = "fa-solid fa-hotel"

class RoomsAdmin(ModelView, model=Rooms):
    column_list = [c.name for c in Rooms.__table__.c] 
    column_list += [Rooms.hotel, Rooms.booking]
    name = "Room"
    name_plural = "Rooms"
    icon = "fa-solid fa-bed"