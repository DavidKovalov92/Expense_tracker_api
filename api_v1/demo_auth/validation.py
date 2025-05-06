import token
from wsgiref import validate
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials,
    OAuth2PasswordBearer,
)
from jwt.exceptions import InvalidTokenError
from fastapi import APIRouter, Form, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from api_v1.demo_auth.helpers import (
    ACCESS_TOKEN_TYPE,
    REFRESH_TOKEN_TYPE,
    create_access_token,
    create_refresh_token,
    TOKEN_TYPE_FIELD,
)
from auth import utils
from ..users.schemas import UserCreate, UserLogin, UserRead
from core.models.db_helper import db_helper
from core.security.hash_password import verify_password
from core.models.models import User

http_bearer = HTTPBearer(auto_error=False)
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/jwt/login",
    auto_error=False,
)

get_db = db_helper.get_scoped_session


def validate_token_type(payload: dict, token_type: str):
    if payload.get(TOKEN_TYPE_FIELD) == token_type:
        return True
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token type",
    )

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
        
        
def get_user_by_token_sub(payload: dict, db: Session):
    if user := db.query(User).filter(User.username == payload.get("sub")).first():
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
    )
        
        
def get_current_auth_user(
    payload: dict = Depends(get_current_token_payload),
    db: Session = Depends(get_db),
):
    validate_token_type(payload, ACCESS_TOKEN_TYPE)
    return get_user_by_token_sub(payload, db)


def get_current_auth_user_for_refresh(
    payload: dict = Depends(get_current_token_payload),
    db: Session = Depends(get_db),
):
    validate_token_type(payload, REFRESH_TOKEN_TYPE)
    return get_user_by_token_sub(payload, db)