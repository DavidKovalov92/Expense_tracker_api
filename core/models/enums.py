from enum import Enum


class ExpenseCategory(Enum):
    GROCERIES = "Groceries"
    LEISURE = "Leisure"
    ELECTRONICS = "Electronics"
    UTILITIES = "Utilities"
    CLOTHING = "Clothing"
    HEALTH = "Health"
    OTHERS = "Others"


class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"
