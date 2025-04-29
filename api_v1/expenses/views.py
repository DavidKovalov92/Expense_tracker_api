import re
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api_v1.expenses import crud
from .schemas import (
    ExpenseCreate,
    ExpenseRead,
)
from core.models.db_helper import db_helper

router = APIRouter(prefix="/api/v1", tags=["Expenses"])

get_db = db_helper.get_scoped_session

@router.get("/expenses/", response_model=ExpenseRead)
def get_expense(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_expenses(db, skip=skip, limit=limit)
