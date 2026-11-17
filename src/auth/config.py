from authx import AuthX, AuthXConfig
from src.config import settings
from src.auth.config import security
from datetime import timedelta
from typing import Annotated
from fastapi import Depends



config = AuthXConfig()

config.JWT_SECRET_KEY = settings.JWT_SECRET_KEY
config.JWT_ALGORITHM = settings.ALGORITHM
config.JWT_TOKEN_LOCATION = ["cookies"]

config.JWT_ACCESS_COOKIE_NAME = "my_access_token"
config.JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

config.JWT_REFRESH_COOKIE_NAME = "my_refresh_token"
config.JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

config.JWT_COOKIE_HTTP_ONLY = True
config.JWT_COOKIE_SECURE = False # for production (https) True, for developing (http) = False
config.JWT_COOKIE_SAMESITE = "lax"

config.JWT_COOKIE_CSRF_PROTECT = True
config.JWT_ACCESS_CSRF_COOKIE_NAME = "csrf_access_token"

security = AuthX(config=config)

AccessRequiredDep = Annotated[None, Depends(security.access_token_required)]
RefreshRequiredDep = Annotated[None, Depends(security.refresh_token_required)]