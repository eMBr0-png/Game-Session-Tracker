from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET_TOKEN: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    STEAM_API_KEY: str

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()