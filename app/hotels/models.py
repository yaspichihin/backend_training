from sqlalchemy import JSON, Column, Integer, String
from sqlalchemy.orm import relationship

from app.db import Base


class Hotels(Base):
    __tablename__ = "hotels"
    id              = Column(Integer, primary_key=True)
    name            = Column(String, nullable=False)
    location        = Column(String, nullable=False)
    services        = Column(JSON)
    rooms_quantity  = Column(Integer, nullable=False)
    image_id        = Column(Integer)


    rooms = relationship("Rooms", back_populates="hotel")

    # Для красивого отображения в Админке 
    def __str__(self):
        return f"Hotel {self.name} {self.location[:30]}"