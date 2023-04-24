from fastapi import Depends, FastAPI
from fastapi.staticfiles import StaticFiles
from routers import users_db, jwt_auth, dicom
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=[
                   "*"],  allow_credentials=True, allow_methods=["*"], allow_headers=["*"], )

app.include_router(users_db.app, prefix="/users", tags=["users"])
app.include_router(jwt_auth.app, prefix="/auth", tags=["jwt_auth"])
app.include_router(dicom.app, prefix="/dicom",
                   tags=["dicom"], dependencies=[Depends(jwt_auth.auth_user)])
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root():
    return {"app": "QMenta challenge"}
