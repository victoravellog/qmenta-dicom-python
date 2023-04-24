from pydantic import BaseModel


class User(BaseModel):
    id: str | None
    username: str
    email: str
    disabled: bool = False
    password: str | None = None


class UserOut(BaseModel):
    id: str
    username: str
    email: str
    disabled: bool = False


class UserInDB(User):
    hashed_password: str | None = ""
