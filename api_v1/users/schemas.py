from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from expenses.schemas import ExpenseRead

        
class UserBase(BaseModel):
    username: str
    email: EmailStr
    
    class Config:
        orm_mode = True
    

class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=255)
    
    
class UserUpdate(UserCreate):
    pass
        
    
class UserRead(UserBase):
    id: int
    created_at: datetime
    expenses: list[ExpenseRead] = []
    
        
class UserOut(UserCreate, UserRead):
    pass