from pathlib import Path
from pydantic import BaseModel
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).parent.parent


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expires_minutes: int = 15
    refresh_token_expires_days: int = 30


class Setting(BaseSettings):
    db_url: str = "postgresql://david:1234@localhost:5432/expense_db"
    auth_jwt: AuthJWT = AuthJWT()


settings = Setting()
