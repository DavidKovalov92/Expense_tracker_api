from typing import List
from pydantic import BaseModel
from sqlalchemy import Enum, ForeignKey
from sqlalchemy import Column, Float, Integer, String, DateTime, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .base import Base
from .enums import ExpenseCategory

class User(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)  # Змінив на id
    username: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)  # Додано унікальність для username
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    expenses: Mapped[list["Expense"]] = relationship("Expense", back_populates="user", cascade="all, delete-orphan", passive_deletes=True)
    
    
class Expense(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)  # Додано первинний ключ для таблиці Expense
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    category: Mapped[ExpenseCategory] = mapped_column(Enum(ExpenseCategory), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user: Mapped[User] = relationship("User", back_populates="expenses")

    
