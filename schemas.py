from pydantic import BaseModel

# ----- Members -----
class MemberCreate(BaseModel):
    name: str

class MemberUpdate(BaseModel):
    name: str


# ----- Deposits -----
class DepositCreate(BaseModel):
    member_id: int
    amount: float

class DepositUpdate(BaseModel):
    amount: float


# ----- Meals -----
class MealCreate(BaseModel):
    member_id: int
    meals: float

class MealUpdate(BaseModel):
    meals: float


# ----- Bazar -----
class BazarCreate(BaseModel):
    member_id: int
    amount: float
    description: str = ""

class BazarUpdate(BaseModel):
    amount: float
    description: str = ""
