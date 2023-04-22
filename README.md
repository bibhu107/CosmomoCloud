## Overview

This project is a user management system that provides APIs to perform several actions such as creating and listing
users, creating and listing organizations, and setting permissions and modifying permission for users on each
organization.

## Problem Statement

You need to build an Access Control / User Management System which needs the features mentioned below. You have to build
APIs for each of these features so that frontend / client can call these APIs and accomplish the task -

1. Create a new User
    - Should have ID, Name, and email. ID can be auto-generated or manually generated.
2. List all users in the system
    - Can filter on the user's name.
    - Should implement pagination using limit & offset, and return the total count of records in each API response, no
      matter what limit.
3. Fetch a single User
4. Create a new Organisation
    - Organisation is a simple bucket entity that can be identified similarly to a Github Organization.
    - Organizations will just have a unique name. No 2 organizations can have the same name.
5. List an organization
    - Can filter on the org’s name.
    - Should implement pagination using limit & offset, and return the total count of records in each API response, no
      matter what limit.
6. Create / Update permissions for Users on each Organization
    - Each User can have access to multiple organizations.
    - Each organization can have multiple users having access to the same.
    - Each User can have different access levels - READ, WRITE, ADMIN
    - Can be a singular API or bulk update/create API - up to you.
7. Remove / Delete permissions for Users on each Organization
    - Can be a singular API or bulk update/create API - up to you.

## Tech Stack Allowed

- Python - FastAPI (preferred), Django or Flask - Mandatory to be python 3
- MongoDB as a database - Using Pymongo / Motor driver, not Django ORM.
- Would not need any other 3rd party libraries, but you can use some simple add ons if required by your solution - No
  major hacks.

-----

## Installation

1. Clone the repository: `gh repo clone bibhu107/CosmomoCloud`
2. Install the required packages: `pip install -r requirements.txt`

## Running the API

Run the following command in your terminal:

```
uvicorn main:app --reload
```

## MongoDB

Make sure you have MongoDB installed on your system. Start the MongoDB server using the following command:

```
mongod
```

## API Endpoints
### Base URL

_Note: This can change as per your system configuration_

#### `http://localhost:8000`

## User Management API

This API provides functionality for managing user information.



#### Create User

Creates a new user in the system.

**Request**

`POST` -
`http://localhost:8000/users`

```
{
    "name": "Bibhu Pala",
    "email": "bibhu.pala@example.com",
    "password": "bibhu_123"
}
```

**Response**

```
{
    "name": "Bibhu Pala",
    "email": "bibhu.pala@example.com",
    "id": "644614d25e247e93b662c3e1",
    "organization_access": null
}
```

#### List Users

In this API call, you can provide queries for name and limit users and put offset.
Returns a list of users in the system.

1. Simple get all users

**Request**

`GET` -
`http://localhost:8000/users`

**Response**

```
{
    "count": 1,
    "limit": 10,
    "offset": 0,
    "data": [
        {
            "name": "Bibhu Pala",
            "email": "bibhu.pala@example.com",
            "id": "644614d25e247e93b662c3e1",
            "organization_access": null
        }
    ]
}

```

2. Adding offset,limit,and name

**Request**

`GET` - `http://localhost:8000/users?name=Bibhu&limit=1&offset=0`

**Response**

```
{
    "count": 1,
    "limit": 1,
    "offset": 0,
    "data": [
        {
            "name": "Bibhu Pala",
            "email": "bibhu.pala@example.com",
            "id": "644614d25e247e93b662c3e1",
            "organization_access": null
        }
    ]
}
```

The `count` field represents the total number of users that match the search criteria.
The `data` field contains an array of users with their `id` and `name` and other informations for users.
The `limit` and `offset` fields represent the maximum number of users to return and the starting index of the returned
users, respectively.

#### Get User

Retrieves information about a specific user.

**Request**

`GET` - `http://localhost:8000/users/1c4f7361-c8c7-473d-85a3-d2ab76981712`

**Response**

```
{
    "name": "Bibhu Pala",
    "email": "bibhu.pala@example.com",
    "id": "644614d25e247e93b662c3e1",
    "organization_access": null
}
```

#### Update User

Updates information about a specific user.

**Request**

`PUT` - `http://localhost:8000/users/644614d25e247e93b662c3e1`

```
{
    "name": "BIBHU PRASAD PALA",
    "email":"bibhu@123.com"
}
```

**Response**

```
{
    "name": "BIBHU PRASAD PALA",
    "email": "bibhu@123.com",
    "id": "644614d25e247e93b662c3e1",
    "organization_access": null
}
```

## Organization Management API

#### Create Organization

Creates a new organization with the provided name.

**Request**

`POST` - `http://localhost:8000/organizations`

```
{
    "name": "Amazon india"
}
```

**Response**

```
{
    "name": "Amazon india",
    "id": "64461d19d3ea1afb77b6ac54",
    "users_id": null
}
```

If an organization with the same name already exists, the API will return an HTTP response with status
code `400 Bad Request`.

#### List Organizations

Lists organizations with optional search by name, limit and offset parameters.

1. Simple get all organization list

**Request**

`GET` - `http://localhost:8000/organizations`

**Response**

```
{
    "count": 2,
    "limit": 10,
    "offset": 0,
    "data": [
        {
            "name": "Amazon india",
            "id": "64461d19d3ea1afb77b6ac54",
            "users_id": null
        },
        {
            "name": "Google india",
            "id": "64461e38d3ea1afb77b6ac55",
            "users_id": null
        }
    ]
}

```

2. Getting organization list based on name and providing pagination with limit and offset

**Request**

`GET` - `http://localhost:8000/organizations?name=goo&limit=10&offset=0`

**Response**

```
{
    "count": 1,
    "limit": 10,
    "offset": 0,
    "data": [
        {
            "name": "Google india",
            "id": "64461e38d3ea1afb77b6ac55",
            "users_id": null
        }
    ]
}
```

The `count` field represents the total number of organizations that match the search criteria. The `data` field contains
an array of organizations with their `id` and `name` fields. The `limit` and `offset` fields represent the maximum
number of organizations to return and the starting index of the returned organizations, respectively.

#### Get Organization

Retrieves information about a specific organization.

**Request**

`GET` - `http://localhost:8000/organizations/64461e38d3ea1afb77b6ac55`

**Response**

```
{
    "name": "Google india",
    "id": "64461e38d3ea1afb77b6ac55",
    "users_id": null
}
```

If the organization does not exist, the API will return an HTTP response with status code `404 Not Found`.

#### Add user to Organization

Adds user to an organization with adding specific access_level

**Request**

`POST` - `http://localhost:8000/organizations/64461d19d3ea1afb77b6ac54/users?access_level=read&user_id=644614d25e247e93b662c3e1`

**Response**

```
{
    "name": "BIBHU PRASAD PALA",
    "email": "bibhu@123.com",
    "id": "644614d25e247e93b662c3e1",
    "organization_access": [
        {
            "organizations_id": "64461d19d3ea1afb77b6ac54",
            "access_level": "read"
        }
    ]
}
```

In this API call, user collection gets a new column `organization_access`
example `[{"organizations_id": "64461d19d3ea1afb77b6ac54", "access_level": "read"}]`
and organization collection gets a new column `users_id` example `["644614d25e247e93b662c3e1"]`.

#### Add user to Organization

Adds user to an organization with adding specific access_level

**Request**

`POST`- `http://localhost:8000/organizations/64461d19d3ea1afb77b6ac54/users?access_level=read&user_id=644614d25e247e93b662c3e1`

**Response**

```
{
    "name": "BIBHU PRASAD PALA",
    "email": "bibhu@123.com",
    "id": "644614d25e247e93b662c3e1",
    "organization_access": [
        {
            "organizations_id": "64461d19d3ea1afb77b6ac54",
            "access_level": "read"
        }
    ]
}
```

In this API call, user collection gets a new column `organization_access`
example `[{"organizations_id": "64461d19d3ea1afb77b6ac54", "access_level": "read"}]`
and organization collection gets a new column `users_id` example `["644614d25e247e93b662c3e1"]`.

#### Update user permission to Organization

This API helps to change permission for a user to an organization. If the user is not linked to the org it raises error.
**Request**

`POST`-`http://localhost:8000/organizations/64461d19d3ea1afb77b6ac54/users/644614d25e247e93b662c3e1/permissions?access_level=admin`

**Response**

```
{
    "name": "BIBHU PRASAD PALA",
    "email": "bibhu@123.com",
    "id": "644614d25e247e93b662c3e1",
    "organization_access": [
        {
            "organizations_id": "64461d19d3ea1afb77b6ac54",
            "access_level": "admin"
        }
    ]
}
```

#### Delete user permission for an Organization

This API helps to deletes permission for a user to an organization. If the user is not linked to the org it raises
error.

`DELETE` - `http://localhost:8000/organizations/64461d19d3ea1afb77b6ac54/users/644614d25e247e93b662c3e1/permissions`

**Response**

```
{
    "name": "BIBHU PRASAD PALA",
    "email": "bibhu@123.com",
    "id": "644614d25e247e93b662c3e1",
    "organization_access": []
}
```

#### Delete user from Organization

This API helps to change permission for a user to a org. If the user is not linked to the org it raises error.

`DELETE` - `http://localhost:8000/organizations/64461d19d3ea1afb77b6ac54/users/644614d25e247e93b662c3e1`

**Response**

```
{
    "name": "BIBHU PRASAD PALA",
    "email": "bibhu@123.com",
    "id": "644614d25e247e93b662c3e1",
    "organization_access": []
}
```

## Error Handling
If an error occurs during the execution of an endpoint, an appropriate error message is returned as the response body. The response status code indicates the type of error that occurred. The possible error codes are:

404 (HTTP_STATUS_CODE_NOT_FOUND): The requested resource could not be found.
500 (STATUS_CODE_INTERNAL_SERVER_ERROR): An unexpected error occurred on the server.


## Database modelling
### sample user collection
```[
  {
    "_id": {"$oid": "644614d25e247e93b662c3e1"},
    "created_at": "2023-04-24 11:04:10",
    "email": "bibhu@123.com",
    "last_updated_at": {"$date": "2023-04-24T05:52:07.884Z"},
    "name": "BIBHU PRASAD PALA",
    "organization_access": [
      {
        "organizations_id": "64461d19d3ea1afb77b6ac54",
        "access_level": "read"
      }
    ],
    "password": "bibhu_123"
  },
  
  {
    "_id": {"$oid": "6446157d5e247e93b662c3e2"},
    "created_at": "2023-04-24 11:07:01",
    "email": "sony.pala@example.com",
    "last_updated_at": "2023-04-24 11:07:01",
    "name": "Sony Pala",
    "password": "sony_123"
  }
]
```

### sample organization collection
```
[
  {
    "_id": {"$oid": "64461d19d3ea1afb77b6ac54"},
    "name": "Amazon india",
    "users_id": ["644614d25e247e93b662c3e1"]
  },
  {
    "_id": {"$oid": "64461e38d3ea1afb77b6ac55"},
    "name": "Google india"
  }
]

```
USER collection has information of Organization it's related with and access_level it has for the organization.
Organization collection stores the users that are part of the organization.
