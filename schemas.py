from pydantic import BaseModel
from datetime import date
from typing import Optional

# ------------------------------
# Members
# ------------------------------
class MemberCreate(BaseModel):
    name: str

class MemberUpdate(BaseModel):
    name: str

# ------------------------------
# Sessions
# ------------------------------
class SessionCreate(BaseModel):
    name: str
    manager: Optional[str] = None
    start_date: date
    end_date: Optional[date] = None

# ------------------------------
# Deposits
# ------------------------------
class DepositCreate(BaseModel):
    member_id: int
    session_id: int
    amount: float
    dep_date: Optional[date] = None  # renamed

class DepositUpdate(BaseModel):
    amount: float
    dep_date: Optional[date] = None  # renamed

# ------------------------------
# Meals
# ------------------------------
class MealCreate(BaseModel):
    member_id: int
    session_id: int
    meals: float
    meal_date: Optional[date] = None  # renamed

class MealUpdate(BaseModel):
    meals: float
    meal_date: Optional[date] = None  # renamed

# ------------------------------
# Bazar
# ------------------------------
class BazarCreate(BaseModel):
    member_id: int
    session_id: int
    amount: float
    description: str = ""
    bazar_date: Optional[date] = None  # renamed

class BazarUpdate(BaseModel):
    amount: float
    description: str = ""
    bazar_date: Optional[date] = None  # renamed
