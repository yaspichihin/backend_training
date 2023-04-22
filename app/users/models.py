from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db import Base


class Users(Base):
    __tablename__ = "users"
    id                  = Column(Integer, primary_key=True)
    email               = Column(String)
    hashed_password     = Column(String)

    booking = relationship("Bookings", back_populates="user")
    
    def __str__(self):
        return f"User {self.email}"
