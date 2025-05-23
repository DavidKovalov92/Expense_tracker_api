from typing import Optional
from api_v1.jwt_auth.validation import get_current_auth_user
from api_v1.limits.validators import (
    is_global_rate_limited,
    is_rate_limited,
    rate_limit_ip,
)
from api_v1.users import crud
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from api_v1.users.dependencies import (
    get_optional_user,
    is_owner_or_admin,
    role_required,
)
from api_v1.users.schemas import (
    UserCreate,
    UserOut,
    UserRead,
)
from celery_worker import save_email_to_folder
from core.models.db_helper import db_helper
from core.models.enums import UserRole
from core.models.models import User
from core.security.hash_password import hash_password


router = APIRouter(prefix="/api/v1", tags=["Users"])

get_db = db_helper.get_scoped_session


@router.get("/users/", response_model=list[UserRead])
def get_users(
    request: Request,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_user),
):
    client_ip = request.client.host if request and request.client else None
    rate_limit_ip(client_ip or "")
    is_global_rate_limited()
    return crud.get_users(db, skip=skip, limit=limit)


@router.get("/users/{user_id}", response_model=UserRead)
def get_user(
    user_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_user),
):
    client_ip = request.client.host if request and request.client else None
    rate_limit_ip(client_ip or "")
    is_global_rate_limited()
    user = crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@router.post("/users/", response_model=UserOut)
def create_user(user_data: UserCreate, request: Request, db: Session = Depends(get_db)):
    client_ip = request.client.host if request and request.client else None
    rate_limit_ip(client_ip or "")

    existing_user = crud.get_user_by_username(db, user_data.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists"
        )

    new_user = crud.create_user(db, user_data)

    subject = "Welcome to our service"
    body = f"Dear {new_user.username},\n\nThank you for registering!"
    to_email = new_user.email
    save_email_to_folder.apply_async(args=[subject, body, to_email])

    return new_user


@router.put("/users/{user_id}", response_model=UserOut)
def update_user(
    user_id: int,
    user_data: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_auth_user),
):
    if current_user is not None:
        is_rate_limited(current_user.id)
    elif current_user is None:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many requests",
        )
    is_global_rate_limited()
    is_owner_or_admin(user_id)(current_user)
    user = crud.update_user(db, user_id, user_data)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@router.patch("/users/{user_id}", response_model=UserOut)
def partial_update_user(
    user_id: int,
    user_data: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_auth_user),
):
    if current_user is not None:
        is_rate_limited(current_user.id)
    elif current_user is None:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many requests",
        )
    is_global_rate_limited()
    is_owner_or_admin(user_id)(current_user)
    user = crud.update_user(db, user_id, user_data)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_auth_user),
):
    if current_user is not None:
        is_rate_limited(current_user.id)
    elif current_user is None:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many requests",
        )
    is_global_rate_limited()
    is_owner_or_admin(user_id)(current_user)
    success = crud.delete_user(db, user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return {"message": "User deleted successfully"}
