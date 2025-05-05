from api_v1.users.schemas import UserCreate
from core.models.models import User
from core.security.hash_password import hash_password
from sqlalchemy.orm import Session

def create_user(db: Session, user_data: UserCreate):
    hashed_password = hash_password(user_data.password)
    user = User(
        username=user_data.username,
        password=hashed_password,
        email=user_data.email,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user(db: Session, user_id: int, user_data: UserCreate):
    user = db.get(User, user_id)
    if not user:
        return None
    if user_data.username is not None:
        user.username = user_data.username
    if user_data.email is not None:
        user.email = user_data.email
        
    db.commit()
    db.refresh(user)
    return user
    


def delete_user(db: Session, user_id: int):
    user = db.get(User, user_id)
    if not user:
        return False
    db.delete(user)
    db.commit()
    return True


def get_user_by_id(db: Session, user_id: int):
    return db.get(User, user_id)


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()
