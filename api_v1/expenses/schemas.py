from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from core.models.enums import ExpenseCategory


class ExpenseBase(BaseModel):
    title: str
    amount: float
    description: str | None = Field(default=None, max_length=255)
    category: ExpenseCategory

    model_config = ConfigDict(from_attributes=True)


class ExpenseCreate(ExpenseBase):
    pass


class ExpenseRead(ExpenseBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ExpenseUpdate(ExpenseBase):
    title: str
    amount: float
    description: str | None = Field(default=None, max_length=255)
    category: ExpenseCategory


class ExpenseOut(ExpenseBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
