from pydantic import BaseModel


class SRooms(BaseModel):
    id: int
    hotel_id: int
    name: str
    description: str|None
    price: int
    services: list[str]
    quantity: int
    image_id: int

    class Config:
        orm_mode = True


class SRoomsRoomLeft(SRooms):
    rooms_left: int
