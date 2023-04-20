from pydantic import BaseModel, EmailStr


class SAuth(BaseModel):
    email:              EmailStr
    hashed_password:    str

    class Config:
        orm_mode = True

class SUsers(SAuth):
    id:     int
