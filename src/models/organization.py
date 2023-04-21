from pydantic import BaseModel

class OrganizationBase(BaseModel):
    name: str

class OrganizationCreate(OrganizationBase):
    pass

class Organization(OrganizationBase):
    id: int
    users: Optional[List[User]] = []

    class Config:
        orm_mode = True
