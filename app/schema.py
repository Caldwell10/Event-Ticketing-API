from pydantic import BaseModel, EmailStr, Field


class UserIn(BaseModel):
    name: str
    phone_number: str = Field(min_length=9)
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        orm_mode = True

class ShowIn(BaseModel):
