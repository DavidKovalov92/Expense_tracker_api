from pydantic_settings import BaseSettings

class Setting(BaseSettings):
    db_url: str = "postgresql://david:1234@localhost:5432/expense_db"
    
    
settings = Setting()
