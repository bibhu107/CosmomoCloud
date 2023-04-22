from typing import List, Optional, Dict, Union

from fastapi import APIRouter

from src.services.user import create_user, list_all_user, get_user_details, update_user_details
from src.models.user import User, UserCreate, UserUpdate

router = APIRouter(prefix="/users")


@router.post("/", response_model=User)
def create_new_user(user: UserCreate):
    print(user)
    return create_user(user)


@router.get("/", response_model=Dict[str, Union[int, List[User]]])
def list_users(name: Optional[str] = None, limit: int = 10, offset: int = 0):
    return list_all_user(name, limit, offset)


@router.get("/{user_id}", response_model=User)
def get_user(user_id: str):
    return get_user_details(user_id)


@router.put("/{user_id}", response_model=User)
def update_user(user_id: str, userUpdated: UserUpdate):
    return update_user_details(user_id, userUpdated)
