import email
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from datetime import datetime
from api_v1.expenses.schemas import ExpenseRead


        
class UserBase(BaseModel):
    username: str
    email: EmailStr | None = None
    
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

