from pydantic import BaseModel, ConfigDict, EmailStr, Field
from datetime import datetime
from api_v1.expenses.schemas import ExpenseRead
from core.models.enums import UserRole


class UserBase(BaseModel):
    username: str
    email: EmailStr | None = None
    role: UserRole = UserRole.USER

    model_config = ConfigDict(from_attributes=True)


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=255)


class UserLogin(UserBase):
    password: str


class UserRead(UserBase):
    id: int
    created_at: datetime
    expenses: list[ExpenseRead] = []


class UserOut(UserCreate, UserRead, UserBase):
    pass
