from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer

from app.auth.auth_schemas import UserSchema, TokenInfo
from app.auth.dependencies import (
    validate_auth_users,
    get_current_active_user,
    get_current_user_for_refresh
)
from app.auth.helpers import create_access_token, create_refresh_token

http_bearer = HTTPBearer(auto_error=False)
auth_router = APIRouter(prefix="/auth", tags=["auth"], dependencies=[Depends(http_bearer)])


@auth_router.post("/login")
async def auth_user(
        user: UserSchema = Depends(validate_auth_users)
) -> TokenInfo:
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)
    return TokenInfo(access_token=access_token, refresh_token=refresh_token)


@auth_router.post("/refresh", response_model_exclude_none=True)
async def refresh_jwt(
        user: UserSchema = Depends(get_current_user_for_refresh)
) -> TokenInfo:
    access_token = create_access_token(user)
    return TokenInfo(access_token=access_token)


@auth_router.get("/me")
async def check_self_info(
        user: UserSchema = Depends(get_current_active_user)
) -> dict:
    return {
        "username": user.username,
        "email": user.email,
        "detail": "ok"
    }
