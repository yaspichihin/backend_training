from sqlalchemy import JSON, Column, ForeignKey, Integer, String
from app.db import Base


class Rooms(Base):
    __tablename__ = "rooms"
    id              = Column(Integer, primary_key=True)
    hotel_id        = Column(ForeignKey("hotels.id"))
    name            = Column(String)
    description     = Column(String)
    price           = Column(Integer)
    services        = Column(JSON)
    quantity        = Column(Integer)
    image_id        = Column(Integer)
