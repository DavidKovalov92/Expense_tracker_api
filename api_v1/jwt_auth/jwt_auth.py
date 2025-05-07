import token
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials,
    OAuth2PasswordBearer,
)
from jwt.exceptions import InvalidTokenError
from fastapi import APIRouter, Form, Depends, HTTPException, Request, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from api_v1.jwt_auth.helpers import (
    ACCESS_TOKEN_TYPE,
    REFRESH_TOKEN_TYPE,
    create_access_token,
    create_refresh_token,
    TOKEN_TYPE_FIELD,
)
from api_v1.jwt_auth.validation import (
    get_current_auth_user,
    get_current_auth_user_for_refresh,
)
from api_v1.limits.validators import is_global_rate_limited, rate_limit_ip
from auth import utils
from ..users.schemas import UserCreate, UserLogin, UserRead
from core.models.db_helper import db_helper
from core.security.hash_password import verify_password
from core.models.models import User
from .validation import http_bearer, oauth2_scheme


class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"


router = APIRouter(
    prefix="/api/v1/jwt",
    tags=["JWT"],
    dependencies=[Depends(http_bearer)],
)
get_db = db_helper.get_scoped_session


def validate_auth_user(
    username: str = Form(),
    password: str = Form(),
    db: Session = Depends(get_db),
) -> UserRead:
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
    )

    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.password):
        raise unauthed_exc

    return UserRead.from_orm(user)


@router.post("/login", response_model=TokenInfo)
def auth_user_issue_jwt(
    request: Request,
    user: UserLogin = Depends(validate_auth_user),
):
    client_ip = request.client.host if request and request.client else None
    rate_limit_ip(client_ip or "")
    is_global_rate_limited()
    access_token = create_access_token(user=user)
    refresh_token = create_refresh_token(user=user)
    return TokenInfo(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.post(
    "/refresh",
    response_model=TokenInfo,
    response_model_exclude_none=True,
)
def auth_refresh_jwt(
    request: Request,
    token: str = Depends(oauth2_scheme),
    user: UserLogin = Depends(get_current_auth_user_for_refresh),
):
    client_ip = request.client.host if request and request.client else None
    rate_limit_ip(client_ip or "")
    is_global_rate_limited()
    access_token = create_access_token(user=user)
    return TokenInfo(
        access_token=access_token,
    )


@router.get("/users/me", response_model=UserRead)
def auth_user_get_me(
    request: Request,
    user: User = Depends(get_current_auth_user),
):
    client_ip = request.client.host if request and request.client else None
    rate_limit_ip(client_ip or "")
    is_global_rate_limited()
    return UserRead.from_orm(user)
