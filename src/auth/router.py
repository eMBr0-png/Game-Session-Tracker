from fastapi import APIRouter, HTTPException, status, Response, Request
from sqlalchemy import select, or_
from src.auth.config import security, config, AccessRequiredDep, RefreshRequiredDep
from src.database import SessionDep
from src.auth.schema import UserRegisterSchema, UserLoginSchema
from src.auth.security import hash_password, verify_password
from src.models import UserModel



router = APIRouter()


@router.post(
    "/register",
    tags=["Authorization"],
    summary="Register",
    status_code=status.HTTP_201_CREATED,
)
async def register(creds: UserRegisterSchema, session: SessionDep, response: Response):
    existing_user_query = select(UserModel).where(
        or_(UserModel.email == creds.email, UserModel.username == creds.username)
    )
    result = await session.execute(existing_user_query)
    
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=400,
            detail="User with this email or username already exists"
        )
    
    hashed_password = hash_password(creds.password)

    new_user = UserModel(
        username=creds.username,
        email=creds.email,
        hashed_password=hashed_password,
    )

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    access_token = security.create_access_token(uid=new_user.id)
    refresh_token = security.create_refresh_token(uid=new_user.id)

    security.set_access_cookies(access_token, response)
    security.set_refresh_cookies(refresh_token, response)

    return {"success": True, "message": "User registered and logged in successfully"}


@router.post(
    "/",
    tags=["Authorization"],
    summary="Login",
)
async def login(creds: UserLoginSchema, session: SessionDep, response: Response):
    query = select(UserModel).where(UserModel.email == creds.email)
    result = await session.execute(query)
    user = result.scalar_one_or_none()

    if user and verify_password(creds.password, user.hashed_password):
        access_token = security.create_access_token(uid=user.id)
        refresh_token = security.create_refresh_token(uid=user.id)

        security.set_access_cookies(access_token, response)
        security.set_refresh_cookies(refresh_token, response)

        return {"success": True, "message": "User logged in successfully"}
    else:
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
        )

@router.delete(
    "/logout",
    tags=["Authorization"],
    summary="Logout"
)
async def logout(request: Request, response: Response, token_required: AccessRequiredDep):
    security.unset_access_cookies(response)
    security.unset_refresh_cookies(response)

    return {"success": True, "message": "User logged out successfully"}

@router.post(
    "/refresh",
    tags=["Authorization"],
    summary="Refresh access and refresh tokens",
)
async def refresh_tokens(request: Request, response: Response, token_requiered: RefreshRequiredDep):
    user_id = security.get_jwt_subject(request)

    new_access_token = security.create_access_token(uid=user_id)
    new_refresh_token = security.create_refresh_token(uid=user_id)

    security.set_access_cookies(new_access_token, response)
    security.set_refresh_cookies(new_refresh_token, response)

    return {"success": True, "message": "Tokens successfully refreshed"}