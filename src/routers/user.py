from fastapi import APIRouter, HTTPException
from bson import ObjectId
from src.models.user import User, UserCreate, UserUpdate
from src.database.database_setup import users

router = APIRouter()


@router.post("/users", response_model=User)
def create_new_user(user: UserCreate):
    user_dict = user.dict()
    user_id = str(users.insert_one(user_dict).inserted_id)
    user_dict['_id'] = user_id
    return User(**user_dict)


@router.get("/users", response_model=List[User])
def list_users(name: Optional[str] = None, limit: int = 10, offset: int = 0):
    query = {}
    if name:
        query['name'] = {'$regex': name, '$options': 'i'}
    cursor = users.find(query).limit(limit).skip(offset)
    user_list = [User(**user) for user in cursor]
    return user_list


@router.get("/users/{user_id}", response_model=User)
def get_user(user_id: str):
    db_user = users.find_one({'_id': ObjectId(user_id)})
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return User(**db_user)


@router.put("/users/{user_id}", response_model=User)
def update_user_details(user_id: str, user: UserUpdate):
    db_user = users.find_one({'_id': ObjectId(user_id)})
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user_dict = user.dict(exclude_unset=True)
    users.update_one({'_id': ObjectId(user_id)}, {'$set': user_dict})
    user_dict['_id'] = user_id
    return User(**user_dict)
