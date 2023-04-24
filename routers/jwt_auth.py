from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from db.models.user import User, UserInDB, UserOut
from db.client import db_client
from db.schemas.user import user_schema, userdb_schema
from config.config import Settings


app = APIRouter()
oauth = OAuth2PasswordBearer(tokenUrl="token")
crypt = CryptContext(schemes=["bcrypt"])
settings = Settings()


async def encrypt_password(password: str) -> str:
    return crypt.hash(password)


async def search_user(field: str, value: str | ObjectId) -> UserInDB:
    try:
        user = db_client.users.find_one({field: value})
        return UserInDB(**userdb_schema(user))
    except:
        return "User not found"


async def auth_user(token: str = Depends(oauth)):
    try:
        decrypted_username = jwt.decode(
            token, settings.SECRET, algorithms=[settings.OAUTH_ALGORITHM]).get("sub")
        user = await search_user("username", decrypted_username)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect token", headers={"WWW-Authenticate": "Bearer"})

    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")

    user_dict = user.dict()
    print(user_dict)
    user_dict['_id'] = user_dict['id']
    del user_dict['password']
    del user_dict['hashed_password']

    return UserOut(**user_schema(user_dict))


async def get_current_user(user: UserOut = Depends(auth_user)):
    return user


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):

    user = await search_user("username", form_data.username)
    if not type(user) == UserInDB:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username")

    if not crypt.verify(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password")

    expire = datetime.utcnow() + timedelta(minutes=int(settings.ACCESS_TOKEN_EXPIRE_MINUTES))

    access_token = jwt.encode({"sub": user.username, "exp": expire},
                              settings.SECRET, algorithm=settings.OAUTH_ALGORITHM)

    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/me")
async def read_users_me(current_user: UserOut = Depends(get_current_user)):
    user = current_user
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect token", headers={"WWW-Authenticate": "Bearer"})

    return current_user
