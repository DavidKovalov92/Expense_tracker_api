from api_v1.expenses.schemas import ExpenseBase, ExpenseCreate
from core.models.models import Expense
from sqlalchemy.orm import Session
from datetime import datetime

def get_expenses(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Expense).offset(skip).limit(limit).all()


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


def get_expenses_for_user(
    db: Session,
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    from_date: datetime | None = None,
    to_date: datetime | None = None
):
    query = db.query(Expense).filter(Expense.user_id == user_id)

    if from_date:
        query = query.filter(Expense.created_at >= from_date)
    if to_date:
        query = query.filter(Expense.created_at <= to_date)

    return query.offset(skip).limit(limit).all()



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