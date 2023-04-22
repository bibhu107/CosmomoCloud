from typing import List, Optional, Union, Dict

from fastapi import APIRouter

from src.models.organization import Organization, OrganizationCreate
from src.models.user import User
from src.services.organization import add_user_to_org_db, delete_user_permission, \
    delete_user_from_organization, create_new_org_store_in_db, list_organizations_with_paging, get_organization_from_db, \
    update_user_permissions_db

router = APIRouter(prefix="/organizations")


@router.post("/", response_model=Organization)
def create_new_organization(org: OrganizationCreate):
    return create_new_org_store_in_db(org);


@router.get("/", response_model=Dict[str, Union[int, List[Organization]]])
def list_organizations(name: Optional[str] = None, limit: int = 10, offset: int = 0):
    return list_organizations_with_paging(name, limit, offset)


@router.get("/{org_id}", response_model=Organization)
def get_organization(org_id: str):
    return get_organization_from_db(org_id)


@router.post("/{org_id}/users", response_model=User)
def add_user_to_org(org_id: str, user_id: str, access_level: str):
    return add_user_to_org_db(org_id, user_id, access_level)


@router.post("/{org_id}/users/{user_id}/permissions", response_model=User)
def update_user_permissions(org_id: str, user_id: str, access_level: str):
    return update_user_permissions_db(org_id, user_id, access_level)


@router.delete("/{org_id}/users/{user_id}/permissions", response_model=User)
def remove_user_permissions(org_id: str, user_id: str):
    return delete_user_permission(org_id, user_id)


@router.delete("/{org_id}/users/{user_id}", response_model=User)
def remove_user_from_org(org_id: str, user_id: str):
    return delete_user_from_organization(org_id, user_id)
