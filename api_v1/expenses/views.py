from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from api_v1.expenses import crud
from .schemas import ExpenseBase, ExpenseCreate, ExpenseRead
from core.models.db_helper import db_helper
from api_v1.demo_auth.validation import get_current_auth_user
from core.models.models import User
from api_v1.users.dependencies import get_optional_user, is_owner_or_admin

router = APIRouter(prefix="/api/v1", tags=["Expenses"])
get_db = db_helper.get_scoped_session


@router.get("/users/{user_id}/expenses/", response_model=list[ExpenseRead])
def get_expense(
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_user)
):
    db_expense = crud.get_expenses_for_user(db, user_id=user_id, skip=skip, limit=limit)
    if not db_expense:
        raise HTTPException(status_code=404, detail="No expenses found")
    return db_expense


@router.post("/users/{user_id}/expenses/", response_model=ExpenseRead)
def create_expense(
    user_id: int,
    expense: ExpenseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_auth_user)
):
    is_owner_or_admin(user_id)(current_user)
    db_expense = crud.create_expense(db=db, user_id=user_id, expense_data=expense)
    return db_expense


@router.put("/users/{user_id}/expenses/{expense_id}", response_model=ExpenseRead)
def update_expense_full(
    user_id: int,
    expense_id: int,
    expense: ExpenseBase,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_auth_user)
):
    is_owner_or_admin(user_id)(current_user)
    db_expense = crud.update_expense(db=db, expense_id=expense_id, expense_data=expense)
    if not db_expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return db_expense


@router.patch("/users/{user_id}/expenses/{expense_id}", response_model=ExpenseRead)
def update_expense(
    user_id: int,
    expense_id: int,
    expense: ExpenseBase,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_auth_user)
):
    is_owner_or_admin(user_id)(current_user)
    db_expense = crud.update_expense(db=db, expense_id=expense_id, expense_data=expense)
    if not db_expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return db_expense


@router.delete("/users/{user_id}/expenses/{expense_id}")
def delete_expense(
    user_id: int,
    expense_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_auth_user)
):
    is_owner_or_admin(user_id)(current_user)
    db_expense = crud.delete_expense(db=db, expense_id=expense_id)
    if not db_expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return {"message": "Deleted successfully"}







