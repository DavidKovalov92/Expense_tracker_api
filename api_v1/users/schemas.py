from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
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
    
    class Config:
        orm_mode = True
        
        
class UserBase(BaseModel):
    username: str
    email: EmailStr
    
    class Config:
        orm_mode = True
    

class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=255)
    
    
class UserUpdate(UserCreate):
    
    class Config:
        orm_mode = True
        
    
class UserRead(UserBase):
    id: int
    created_at: datetime
    expenses: list[ExpenseRead] = []
    
    class Config:
        orm_mode = True
        
        
class UserOut(UserCreate, UserRead):
    class Config:
        orm_mode = True