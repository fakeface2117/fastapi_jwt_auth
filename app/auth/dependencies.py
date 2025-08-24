from typing import Callable

from fastapi import Form, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError

from app.auth.auth_schemas import UserSchema
from app.auth.database import user_db
from app.auth.helpers import TOKEN_TYPE_FIELD, ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE
from app.auth.utils import validate_password, decode_jwt

# указывается адрес для выпуска токена
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def validate_auth_users(
        username: str = Form(),
        password: str = Form(),
) -> UserSchema:
    if username not in user_db:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    if not validate_password(password, user_db[username].password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    if not user_db[username].active:
        raise HTTPException(status_code=403, detail="User is not active")
    return user_db[username]


def validate_token_type(payload: dict, token_type: str) -> bool:
    current_token_type = payload.get(TOKEN_TYPE_FIELD)
    if current_token_type == token_type:
        return True
    raise HTTPException(status_code=401, detail=f"Invalid token type '{current_token_type}' expected '{token_type}'")


def get_user_by_token_sub(payload: dict) -> UserSchema:
    username: str | None = payload.get("sub")
    if username not in user_db:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user_db[username]


def get_auth_user_from_token_type(token_type: str) -> Callable:
    def get_user_from_token(
            token: str = Depends(oauth2_scheme)
    ) -> UserSchema:
        try:
            payload = decode_jwt(token)
        except InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token error")
        validate_token_type(payload, token_type)
        return get_user_by_token_sub(payload)

    return get_user_from_token


get_current_user = get_auth_user_from_token_type(ACCESS_TOKEN_TYPE)

get_current_user_for_refresh = get_auth_user_from_token_type(REFRESH_TOKEN_TYPE)


def get_current_active_user(
        user: UserSchema = Depends(get_current_user)
) -> UserSchema:
    if user.active:
        return user
    raise HTTPException(status_code=403, detail="Inactive user")
