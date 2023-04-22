from pydantic import BaseModel, EmailStr


class SAuth(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode = True


class SUsers(SAuth):
    id: int
