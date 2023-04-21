from fastapi import APIRouter, Depends, HTTPException
from pymongo import MongoClient
from bson import ObjectId
from typing import List, Optional

from schemas.organization import Organization, OrganizationCreate
from crud.organization import create_organization, get_organization_by_id, get_organizations

router = APIRouter()

client = MongoClient("mongodb://localhost:27017/")
db = client["mydatabase"]
collection = db["organizations"]

@router.post("/organizations", response_model=Organization)
def create_new_organization(org: OrganizationCreate):
    db_org = dict(org)
    result = collection.insert_one(db_org)
    db_org["_id"] = str(result.inserted_id)
    return db_org

@router.get("/organizations", response_model=List[Organization])
def list_organizations(name: Optional[str] = None, limit: int = 10, offset: int = 0):
    query = {}
    if name:
        query["name"] = name
    organizations = collection.find(query).skip(offset).limit(limit)
    return list(organizations)

@router.get("/organizations/{org_id}", response_model=Organization)
def get_organization(org_id: str):
    organization = collection.find_one({"_id": ObjectId(org_id)})
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")
    return organization
