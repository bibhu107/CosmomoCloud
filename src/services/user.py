import traceback
from datetime import datetime
from typing import Optional

from bson import ObjectId
from bson import json_util
from fastapi import HTTPException

from src.database.database_setup import users
from src.models.user import User, UserCreate, UserUpdate, UserNotFoundException
from src.utilities.Constants import STATUS_CODE_INTERNAL_SERVER_ERROR, \
    DB_ID_KEY, ID


def create_user(user: UserCreate):
    try:
        user_dict = user.dict()
        user_dict['created_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        user_dict['last_updated_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        result = users.insert_one(user_dict)
        print(result)
        user_dict[ID] = str(result.inserted_id)
        return User(**user_dict)
    except Exception as e:
        raise HTTPException(status_code=STATUS_CODE_INTERNAL_SERVER_ERROR, detail=str(e))


def list_all_user(name: Optional[str] = None, limit: int = 10, offset: int = 0):
    try:
        query = {}
        if name:
            query['name'] = {'$regex': name, '$options': 'i'}
        count = users.count_documents(query)
        cursor = users.find(query).limit(limit).skip(offset)
        user_list = []
        for user in cursor:
            user_dict = user.copy()
            user_dict[ID] = str(user_dict.pop(DB_ID_KEY))
            user_list.append(User.parse_raw(json_util.dumps(user_dict)))
        response = {
            'count': count,
            'limit': limit,
            'offset': offset,
            'data': user_list
        }
        return response
    except Exception as e:
        raise HTTPException(status_code=STATUS_CODE_INTERNAL_SERVER_ERROR, detail=str(e))


def get_user_details(user_id: str):
    try:
        user_id = user_id.strip()
        db_user = users.find_one({DB_ID_KEY: ObjectId(user_id)})
        if db_user is None:
            raise UserNotFoundException(user_id)
        db_user[ID] = str(db_user.pop(DB_ID_KEY))
        return User(**db_user)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=STATUS_CODE_INTERNAL_SERVER_ERROR, detail=str(e))


def update_user_details(user_id: str, userUpdated: UserUpdate):
    try:
        original_user_id = user_id.strip()
        db_user = users.find_one({DB_ID_KEY: ObjectId(original_user_id)})
        print(db_user)
        if db_user is None:
            raise UserNotFoundException(original_user_id)
        user_updated_dict = userUpdated.dict(exclude_unset=True)
        user_updated_dict["last_updated_at"] = datetime.utcnow()
        print(user_updated_dict)
        users.update_one({DB_ID_KEY: ObjectId(original_user_id)}, {'$set': user_updated_dict})
        user_updated_dict[ID] = user_id
        return User(**user_updated_dict)
    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=STATUS_CODE_INTERNAL_SERVER_ERROR, detail=str(e))
