from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials,
    OAuth2PasswordBearer,
)
from jwt.exceptions import InvalidTokenError
from fastapi import APIRouter, Form, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from auth import utils
from ..users.schemas import UserCreate, UserLogin, UserRead
from core.models.db_helper import db_helper
from core.security.hash_password import verify_password
from core.models.models import User

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/jwt/login",
)


class TokenInfo(BaseModel):
    access_token: str
    token_type: str


router = APIRouter(prefix="/api/v1/jwt", tags=["JWT"])
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


def get_current_token_payload(
    token: str = Depends(oauth2_scheme),
):
    try:
        return utils.decode_jwt(token=token)
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        ) from e


def get_current_auth_user(
    payload: dict = Depends(get_current_token_payload),
    db: Session = Depends(get_db),
):
    if user := db.query(User).filter(User.username == payload.get("sub")).first():
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
    )


@router.post("/login", response_model=TokenInfo)
def auth_user_issue_jwt(user: UserLogin = Depends(validate_auth_user)):
    return TokenInfo(
        access_token=utils.encode_jwt(
            {
                "sub": user.username,
                "username": user.username,
                "email": user.email,
            }
        ),
        token_type="Bearer",
    )


@router.get("/users/me", response_model=UserRead)
def auth_user_get_me(user: User = Depends(get_current_auth_user)):
    return UserRead.from_orm(user)
