import traceback
from typing import Optional

from fastapi import HTTPException

from src.database.database_setup import organizations, users
from src.models.organization import OrganizationCreate, OrganizationNotFoundException
from src.models.user import User, UserNotFoundException
from src.utilities import Constants
from src.utilities.Constants import HTTP_STATUS_CODE_NOT_FOUND, MISSING_RECORD_FAILED_TO_UPDATE, \
    STATUS_CODE_INTERNAL_SERVER_ERROR, DB_ID_KEY, MISSING_RECORD_FAILED_TO_DELETE, \
    USER_MISSING_FROM_ORG, DUPLICATE_ORGANIZATION, ID
from src.utilities.database_utilities import get_data_from_id, get_object_id, get_striped_id


def create_new_org_store_in_db(org: OrganizationCreate):
    try:
        # Check if an organization with the same name already exists
        existing_org = organizations.find_one({"name": org.name})
        if existing_org:
            raise HTTPException(status_code=HTTP_STATUS_CODE_NOT_FOUND, detail=DUPLICATE_ORGANIZATION)
        # Create a new organization with the given name
        db_org = dict(org)
        result = organizations.insert_one(db_org)
        db_org[ID] = str(result.inserted_id)
        return db_org
    except Exception as e:
        raise HTTPException(status_code=STATUS_CODE_INTERNAL_SERVER_ERROR, detail=str(e))


def list_organizations_with_paging(name: Optional[str], limit: int, offset: int):
    try:
        query = {}
        if name:
            query['name'] = {'$regex': name, '$options': 'i'}
        orgs = organizations.find(query).skip(offset).limit(limit)
        org_list = [{ID: str(org[DB_ID_KEY]), "name": org["name"]} for org in orgs]
        total_count = organizations.count_documents(query)
        response = {
            'count': total_count,
            'limit': limit,
            'offset': offset,
            'data': org_list
        }
        return response
    except Exception as e:
        raise HTTPException(status_code=STATUS_CODE_INTERNAL_SERVER_ERROR, detail=str(e))


def get_organization_from_db(org_id: str):
    try:
        organization = organizations.find_one({DB_ID_KEY: get_object_id(org_id)})
        if not organization:
            raise OrganizationNotFoundException(get_striped_id(org_id))
        organization[ID] = str(organization.pop(DB_ID_KEY))
        return organization
    except Exception as e:
        raise HTTPException(status_code=STATUS_CODE_INTERNAL_SERVER_ERROR, detail=str(e))


def add_user_to_org_db(org_id: str, user_id: str, access_level: str):
    try:
        org, user = _get_org_and_user(org_id, user_id)
        striped_org_id, striped_user_id, = _get_striped_org_and_user_id(org_id, user_id)
        access_level = get_striped_id(access_level)
        # Add organization access to user if it doesn't exist
        if Constants.ORGNIZATIONS_ID_ACCESS_LEVEL_KEY not in user:
            user[Constants.ORGNIZATIONS_ID_ACCESS_LEVEL_KEY] = []
        org_access_exists = False
        for access in user[Constants.ORGNIZATIONS_ID_ACCESS_LEVEL_KEY]:
            if access[Constants.ORGANIZATIONS_ID_KEY] == striped_org_id:
                # Update access level if organization access already exists
                access[Constants.ACCESS_LEVEL_ID_KEY] = access_level
                org_access_exists = True
                break
        if not org_access_exists:
            # Add organization access to user
            user[Constants.ORGNIZATIONS_ID_ACCESS_LEVEL_KEY].append({
                Constants.ORGANIZATIONS_ID_KEY: striped_org_id,
                Constants.ACCESS_LEVEL_ID_KEY: access_level
            })

        # Update user in database
        users.update_one({DB_ID_KEY: get_object_id(user_id)}, {
            '$set': {Constants.ORGNIZATIONS_ID_ACCESS_LEVEL_KEY: user[Constants.ORGNIZATIONS_ID_ACCESS_LEVEL_KEY]}})
        # Add user to organization if not already a member
        if Constants.USERS_ID_KEY not in org:
            org[Constants.USERS_ID_KEY] = []
        if striped_user_id not in org[Constants.USERS_ID_KEY]:
            org[Constants.USERS_ID_KEY].append(striped_user_id)
            organizations.update_one({DB_ID_KEY: get_object_id(org_id)},
                                     {'$set': {Constants.USERS_ID_KEY: org[Constants.USERS_ID_KEY]}})
        # Convert dictionary to User object
        user[ID] = striped_user_id
        user_obj = User(**user)
        print(user_obj)
        return user_obj
    except Exception as e:
        print(traceback.format_exc())  # add this line to print the traceback
        raise HTTPException(status_code=STATUS_CODE_INTERNAL_SERVER_ERROR, detail=str(e))


def update_user_permissions_db(org_id: str, user_id: str, access_level: str):
    try:
        org, user = _get_org_and_user(org_id, user_id)
        striped_org_id, striped_user_id = _get_striped_org_and_user_id(org_id, user_id)
        access_level = get_striped_id(access_level)
        # Add organization access to user if it doesn't exist
        if Constants.ORGNIZATIONS_ID_ACCESS_LEVEL_KEY not in user:
            raise HTTPException(status_code=HTTP_STATUS_CODE_NOT_FOUND, detail=MISSING_RECORD_FAILED_TO_UPDATE)
        org_access_exists = False
        for access in user[Constants.ORGNIZATIONS_ID_ACCESS_LEVEL_KEY]:
            if access[Constants.ORGANIZATIONS_ID_KEY] == striped_org_id:
                # Update access level if organization access already exists
                access[Constants.ACCESS_LEVEL_ID_KEY] = access_level
                org_access_exists = True
                break
        if not org_access_exists:
            raise HTTPException(status_code=HTTP_STATUS_CODE_NOT_FOUND, detail=MISSING_RECORD_FAILED_TO_UPDATE)

        # Update user in database
        users.update_one({DB_ID_KEY: get_object_id(user_id)}, {
            '$set': {Constants.ORGNIZATIONS_ID_ACCESS_LEVEL_KEY: user[Constants.ORGNIZATIONS_ID_ACCESS_LEVEL_KEY]}})
        # Return updated user object
        user[ID] = striped_user_id
        return User(**user)
    except Exception as e:
        raise HTTPException(status_code=STATUS_CODE_INTERNAL_SERVER_ERROR, detail=str(e))


def delete_user_permission(org_id: str, user_id: str):
    try:
        org, user = _get_org_and_user(org_id, user_id)
        striped_org_id, striped_user_id, = _get_striped_org_and_user_id(org_id, user_id)
        # Remove user from organization
        organizations.update_one({DB_ID_KEY: get_object_id(org_id)},
                                 {"$pull": {Constants.USERS_ID_KEY: striped_user_id}})
        # Remove organization access from user
        org_access_exists = False
        for access in user[Constants.ORGNIZATIONS_ID_ACCESS_LEVEL_KEY]:
            if access[Constants.ORGANIZATIONS_ID_KEY] == striped_org_id:
                user[Constants.ORGNIZATIONS_ID_ACCESS_LEVEL_KEY].remove(access)
                org_access_exists = True
                break

        if not org_access_exists:
            raise HTTPException(status_code=HTTP_STATUS_CODE_NOT_FOUND, detail=MISSING_RECORD_FAILED_TO_DELETE)
        # Update user in database
        users.update_one({DB_ID_KEY: get_object_id(user_id)}, {
            "$set": {Constants.ORGNIZATIONS_ID_ACCESS_LEVEL_KEY: user[Constants.ORGNIZATIONS_ID_ACCESS_LEVEL_KEY]}})
        # Convert dictionary to User object
        user[ID] = striped_user_id
        user_obj = User(**user)
        return user_obj
    except Exception as e:
        raise HTTPException(status_code=STATUS_CODE_INTERNAL_SERVER_ERROR, detail=str(e))


def delete_user_from_organization(org_id: str, user_id: str):
    try:
        org, user = _get_org_and_user(org_id, user_id)
        striped_org_id, striped_user_id, = _get_striped_org_and_user_id(org_id, user_id)
        if Constants.ORGNIZATIONS_ID_ACCESS_LEVEL_KEY not in user:
            raise HTTPException(status_code=HTTP_STATUS_CODE_NOT_FOUND, detail=USER_MISSING_FROM_ORG)
        if org_id not in [access[Constants.ORGANIZATIONS_ID_KEY] for access in
                          user[Constants.ORGNIZATIONS_ID_ACCESS_LEVEL_KEY]]:
            raise HTTPException(status_code=HTTP_STATUS_CODE_NOT_FOUND, detail=USER_MISSING_FROM_ORG)
        user[Constants.ORGNIZATIONS_ID_ACCESS_LEVEL_KEY] = [access for access in
                                                            user[Constants.ORGNIZATIONS_ID_ACCESS_LEVEL_KEY]
                                                            if access[Constants.ORGANIZATIONS_ID_KEY] != org_id]
        users.update_one({DB_ID_KEY: get_object_id(user_id)},
                         {"$set": {Constants.ORGNIZATIONS_ID_ACCESS_LEVEL_KEY: user[
                             Constants.ORGNIZATIONS_ID_ACCESS_LEVEL_KEY]}})

        # Remove user ID from the organization's user IDs list
        if Constants.USERS_ID_KEY in org:
            if striped_user_id in org[Constants.USERS_ID_KEY]:
                org[Constants.USERS_ID_KEY].remove(striped_user_id)
                organizations.update_one({DB_ID_KEY: get_object_id(org_id)},
                                         {"$set": {Constants.USERS_ID_KEY: org[Constants.USERS_ID_KEY]}})
            else:
                raise HTTPException(status_code=HTTP_STATUS_CODE_NOT_FOUND, detail=USER_MISSING_FROM_ORG)
        else:
            raise HTTPException(status_code=HTTP_STATUS_CODE_NOT_FOUND, detail=USER_MISSING_FROM_ORG)
        user['id'] = striped_user_id
        return User(**user)
    except Exception as e:
        print(traceback.format_exc())  # add this line to print the traceback
        raise HTTPException(status_code=STATUS_CODE_INTERNAL_SERVER_ERROR, detail=str(e))


def _get_org_and_user(org_id: str, user_id: str):
    org = get_data_from_id(organizations, org_id)
    if org is None:
        raise OrganizationNotFoundException(get_striped_id(org_id))
    user = get_data_from_id(users, user_id)
    if user is None:
        raise UserNotFoundException(get_striped_id(user_id))
    return org, user


def _get_striped_org_and_user_id(org_id: str, user_id: str):
    return get_striped_id(org_id), get_striped_id(user_id)
