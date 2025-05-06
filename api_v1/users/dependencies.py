from fastapi import Depends, HTTPException, Security, status
from sqlalchemy.orm import Session
from typing import Optional, List
from enum import Enum
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from functools import wraps

from api_v1.demo_auth.validation import get_current_auth_user
from core.models.enums import UserRole
from core.models.models import User
from api_v1.demo_auth.validation import http_bearer


def role_required(required_roles: List[UserRole]):
    def wrapper(user: User = Depends(get_current_auth_user)):
        if user.role not in required_roles and user.role != UserRole.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Requires one of these roles: {', '.join(required_roles)}",
            )
        return user

    return wrapper


# Альтернатива: декоратор для проверки аутентификации + ролей
def auth_required(required_roles: Optional[List[UserRole]] = None):
    def decorator(endpoint):
        @wraps(endpoint)
        async def wrapped(*args, **kwargs):
            # Проверяем аутентификацию
            user = get_current_auth_user()

            # Проверяем роли (если указаны)
            if (
                required_roles
                and user.role not in required_roles
                and user.role != UserRole.ADMIN
            ):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Insufficient permissions",
                )

            return await endpoint(*args, **kwargs, current_user=user)

        return wrapped

    return decorator


def is_owner_or_admin(resource_owner_id: int):
    def wrapper(current_user: User = Depends(get_current_auth_user)):
        if current_user.id != resource_owner_id and current_user.role != UserRole.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only access your own resources",
            )
        return current_user

    return wrapper


def get_optional_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Security(http_bearer),
):
    if credentials is None:
        return None
    return get_current_auth_user({"token": credentials})
