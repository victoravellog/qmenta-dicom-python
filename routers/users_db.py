from fastapi import APIRouter, Depends, HTTPException, status
from db.models.user import User, UserInDB, UserOut
from db.schemas.user import user_schema, users_schema
from db.client import db_client
from bson import ObjectId
from routers.jwt_auth import encrypt_password
from routers import jwt_auth

app = APIRouter()


@app.get("/", response_model=list[UserOut], dependencies=[Depends(jwt_auth.auth_user)])
async def users():
    users = db_client.users.find()
    return users_schema(users)


@app.get("/{user_id}", response_model=UserOut, dependencies=[Depends(jwt_auth.auth_user)])
async def user(user_id: str):
    try:
        user = await search_user("_id", ObjectId(user_id))
        return user
    except:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="User not found")


@app.post("/", status_code=status.HTTP_201_CREATED, response_model=UserOut)
async def create_user(user: User):
    # check if user already exists
    if not (await search_user("email", user.email) == "User not found" and await search_user("username", user.username) == "User not found"):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="User already exists")
    user = UserInDB(**user.dict())
    user.hashed_password = str(await encrypt_password(user.password))
    user_dict = user.dict()
    del user_dict['password']
    del user_dict['id']

    id = db_client.users.insert_one(
        user_dict).inserted_id
    new_user = db_client.users.find_one({"_id": id})
    return UserOut(**user_schema(new_user))


@app.put("/{user_id}", response_model=UserOut, dependencies=[Depends(jwt_auth.auth_user)])
async def update_user(user_id: str, user: User):
    try:
        user_dict = user.dict()
        del user_dict['id']

        db_client.users.find_one_and_replace(
            {"_id": ObjectId(user_id)}, user_dict)
    except:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="User not found")

    return await search_user("_id", ObjectId(user_id))


@app.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(jwt_auth.auth_user)])
async def delete_user(user_id: str):
    try:
        db_client.users.delete_one({"_id": ObjectId(user_id)})
        return None
    except:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="User not found")


async def search_user(field: str, value: str | ObjectId):
    try:
        user = db_client.users.find_one({field: value})
        return UserOut(**user_schema(user))
    except:
        return "User not found"
