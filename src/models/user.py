from typing import Optional
from pydantic import BaseModel

class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    password: Optional[str]

class User(UserBase):
    id: int
    organizations: Optional[List[Organization]] = []

    class Config:
        orm_mode = True
