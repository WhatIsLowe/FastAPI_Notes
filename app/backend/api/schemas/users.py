from pydantic import BaseModel, constr
from typing import Optional


class UserCreateSchema(BaseModel):
    username: constr(min_length=3, max_length=50)
    hashed_password: str
    phone_number: constr(min_length=10, max_length=15)


class UserUpdateSchema(BaseModel):
    username: Optional[constr(min_length=3, max_length=50)] = None
    hashed_password: Optional[str] = None
    phone_number: Optional[constr(min_length=10, max_length=15)] = None


class UserSchema(BaseModel):
    id: int
    username: str
    phone_number: str

    class Config:
        orm_mode = True
