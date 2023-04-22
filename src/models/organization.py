from typing import List
from fastapi.exceptions import HTTPException

from pydantic import BaseModel
from pydantic.class_validators import Optional

from src.utilities.Constants import HTTP_STATUS_CODE_NOT_FOUND


class OrganizationBase(BaseModel):
    name: str


class OrganizationCreate(OrganizationBase):
    pass


class Organization(OrganizationBase):
    id: str
    users_id: Optional[List[str]]

    class Config:
        orm_mode = True


class OrganizationNotFoundException(HTTPException):
    def __init__(self, org_id: str):
        detail = f"Org {org_id} not found"
        super().__init__(status_code=HTTP_STATUS_CODE_NOT_FOUND, detail=detail)
