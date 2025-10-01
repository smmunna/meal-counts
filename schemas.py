from pydantic import BaseModel
from datetime import date

# ----- Members -----
class MemberCreate(BaseModel):
    name: str

class MemberUpdate(BaseModel):
    name: str


# ----- Sessions -----
class SessionCreate(BaseModel):
    name: str
    manager: str = None
    start_date: date
    end_date: date = None


# ----- Deposits -----
class DepositCreate(BaseModel):
    member_id: int
    session_id: int
    amount: float
    date: date = None

class DepositUpdate(BaseModel):
    amount: float
    date: date = None


# ----- Meals -----
class MealCreate(BaseModel):
    member_id: int
    session_id: int
    meals: float
    date: date = None

class MealUpdate(BaseModel):
    meals: float
    date: date = None


# ----- Bazar -----
class BazarCreate(BaseModel):
    member_id: int
    session_id: int
    amount: float
    description: str = ""
    date: date = None

class BazarUpdate(BaseModel):
    amount: float
    description: str = ""
    date: date = None
