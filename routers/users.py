from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

app = APIRouter()


class User(BaseModel):
    id: int
    name: str
    surname: str
    url: str
    age: int


users_list = [
    User(id=1, name="John", surname="Doe", url="https://example.com", age=42),
    User(id=2, name="Jane", surname="Doe", url="https://example.com", age=42),
]


@app.get("/")
async def users():
    return users_list


@app.get("/{user_id}", response_model=User)
async def user(user_id: int):
    try:
        return await search_user(user_id)
    except:
        raise HTTPException(status_code=422, detail="User not found")


@app.post("/", status_code=201, response_model=User)
async def create_user(user: User):
    if not type(await search_user(user.id)) == User:
        users_list.append(user)
        return user

    raise HTTPException(status_code=400, detail="User already exists")


@app.put("/{user_id}", response_model=User)
async def update_user(user_id: int, user: User):
    try:
        user_to_update = await search_user(user_id)
        user_to_update.name = user.name
        user_to_update.surname = user.surname
        user_to_update.url = user.url
        user_to_update.age = user.age
        return user_to_update
    except:
        raise HTTPException(status_code=422, detail="User not found")


@app.patch("/{user_id}", response_model=User)
async def update_user(user_id: int, user: User):
    try:
        user_to_update = await search_user(user_id)
        if user.name:
            user_to_update.name = user.name
        if user.surname:
            user_to_update.surname = user.surname
        if user.url:
            user_to_update.url = user.url
        if user.age:
            user_to_update.age = user.age
        return user_to_update
    except:
        raise HTTPException(status_code=422, detail="User not found")


@app.delete("/{user_id}", status_code=204)
async def delete_user(user_id: int):
    try:
        user_to_delete = await search_user(user_id)
        users_list.remove(user_to_delete)
        return {"message": "User deleted"}
    except:
        raise HTTPException(status_code=422, detail="User not found")


async def search_user(user_id):
    try:
        users = filter(lambda user: user.id == user_id, users_list)
        return list(users)[0]
    except:
        return None
