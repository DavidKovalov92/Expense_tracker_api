from api_v1.users.schemas import ExpenseBase, ExpenseCreate, UserCreate, UserUpdate
from core.models.models import Expense, User
from core.security.hash_password import hash_password
from sqlalchemy.orm import Session


def get_expenses(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Expense).offset(skip).limit(limit).all()



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


def update_user(db: Session, user_id: int, user_data: UserUpdate):
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


def create_expense(db: Session, user_id: int, expense_data: ExpenseCreate):
    expense = Expense(
        title=expense_data.title,
        amount=expense_data.amount,
        description=expense_data.description,
        category=expense_data.category,
        user_id=user_id,
    )
    db.add(expense)
    db.commit()
    db.refresh(expense)
    return expense


def get_expense_by_id(db: Session, expense_id: int):
    return db.get(Expense, expense_id)


def get_expenses_for_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(Expense).filter(Expense.user_id == user_id).offset(skip).limit(limit).all()


def update_expense(db: Session, expense_id: int, expense_data: ExpenseBase):
    expense = db.get(Expense, expense_id)
    if not expense:
        return None
    if expense_data.title is not None:
        expense.title = expense_data.title
    if expense_data.amount is not None:
        expense.amount = expense_data.amount
    if expense_data.description is not None:
        expense.description = expense_data.description
    if expense_data.category is not None:
        expense.category = expense_data.category
        
    db.commit()
    db.refresh(expense)
    return expense
    

def delete_expense(db: Session, expense_id: int):
    expense = db.get(Expense, expense_id)
    if not expense:
        return False
    db.delete(expense)
    db.commit()
    return True