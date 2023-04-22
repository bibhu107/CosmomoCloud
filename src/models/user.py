from fastapi.exceptions import HTTPException
from typing import Optional, List

from pydantic import BaseModel
from src.utilities.Constants import HTTP_STATUS_CODE_NOT_FOUND, USER_NOT_FOUND, STATUS_CODE_INTERNAL_SERVER_ERROR


class UserBase(BaseModel):
    name: str
    email: str


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    password: Optional[str]


class OrganizationsAccess(BaseModel):
    organizations_id: str
    access_level: str


class User(UserBase):
    id: str
    organization_access: Optional[List[OrganizationsAccess]]

    class Config:
        orm_mode = True


class UserNotFoundException(HTTPException):
    def __init__(self, user_id: str):
        detail = f"User {user_id} not found"
        super().__init__(status_code=HTTP_STATUS_CODE_NOT_FOUND, detail=detail)
