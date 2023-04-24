from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "QMenta challenge"
    OAUTH_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: str
    SECRET: str
    MONGO_CONNECTION: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
