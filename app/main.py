from fastapi import FastAPI 
from fastapi import Depends
from fastapi import Query           # для логической валидации данных
from typing import Optional         # для указания опциональных параметров
from datetime import date           # для указания типа данных date
from pydantic import BaseModel      # для валидации и схемы данных

# Импорт роутеров
from app.bookings.router import router as router_bookings
from app.users.router import router_auth as router_auth
from app.users.router import router_user as router_user
from app.hotels.router import router as router_hotels
from app.hotels.rooms.router import router as router_rooms

app =  FastAPI()
# Добавление роутеров
app.include_router(router_auth)
app.include_router(router_user)
app.include_router(router_bookings)
app.include_router(router_hotels)
app.include_router(router_rooms)