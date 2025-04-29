from datetime import datetime
from pydantic import BaseModel, Field
from core.models.enums import ExpenseCategory

class ExpenseBase(BaseModel):
    title: str
    amount: float
    description: str | None = Field(default=None, max_length=255)
    category: ExpenseCategory
    
    class Config:
        orm_mode = True
    
    
class ExpenseCreate(ExpenseBase):
    pass


class ExpenseRead(ExpenseBase):
    id: int
    created_at: datetime
    
        
        
class ExpenseUpdate(ExpenseBase):
    title: str
    amount: float
    description: str | None = Field(default=None, max_length=255)
    category: ExpenseCategory
    
    
class ExpenseOut(ExpenseBase): 
    id: int
    created_at: datetime

        