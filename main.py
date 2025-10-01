from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
import models
from database import engine, SessionLocal, Base
from fastapi import Path
from fastapi import Body

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ------------------------------
# Schemas (Pydantic models)
# ------------------------------
class MemberCreate(BaseModel):
    name: str


class DepositCreate(BaseModel):
    member_id: int
    amount: float


class MealCreate(BaseModel):
    member_id: int
    meals: float

class BazarCreate(BaseModel):
    member_id: int
    amount: float
    description: str = ""

# ------------------------------
# Routes
# ------------------------------
@app.post("/members/")
def create_member(member: MemberCreate, db: Session = Depends(get_db)):
    db_member = models.Member(name=member.name)
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member


@app.post("/deposit/")
def create_deposit(deposit: DepositCreate, db: Session = Depends(get_db)):
    member = db.query(models.Member).filter(models.Member.id == deposit.member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    db_deposit = models.Deposit(member_id=deposit.member_id, amount=deposit.amount)
    db.add(db_deposit)
    db.commit()
    db.refresh(db_deposit)
    return db_deposit


@app.post("/meal/")
def create_meal(meal: MealCreate, db: Session = Depends(get_db)):
    member = db.query(models.Member).filter(models.Member.id == meal.member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    db_meal = models.Meal(member_id=meal.member_id, meals=meal.meals)
    db.add(db_meal)
    db.commit()
    db.refresh(db_meal)
    return db_meal


@app.post("/bazar/")
def add_bazar(bazar: BazarCreate, db: Session = Depends(get_db)):
    member = db.query(models.Member).filter(models.Member.id == bazar.member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    db_bazar = models.Bazar(
        member_id=bazar.member_id,
        amount=bazar.amount,
        description=bazar.description
    )
    db.add(db_bazar)
    db.commit()
    db.refresh(db_bazar)
    return db_bazar


@app.get("/meal-stats/")
def meal_stats(db: Session = Depends(get_db)):
    members = db.query(models.Member).all()

    # Total bazar spent (all bazar entries)
    total_bazar = sum(b.amount for b in db.query(models.Bazar).all())

    # Total deposits (all member deposits)
    total_deposit = sum(d.amount for d in db.query(models.Deposit).all())

    # Total meals (sum of all member meals)
    total_meals = sum(sum(me.meals for me in m.meals) for m in members)

    # Meal rate = cost per meal
    meal_rate = total_bazar / total_meals if total_meals > 0 else 0

    # Total meal cost (based on total meals × rate)
    total_meal_cost = total_meals * meal_rate

    results = []
    overall_in_hand = 0  # sum of all members’ in-hand

    for m in members:
        member_deposit = sum(d.amount for d in m.deposits)
        member_meals = sum(me.meals for me in m.meals)
        meal_cost = member_meals * meal_rate
        in_hand = member_deposit - meal_cost

        overall_in_hand += in_hand

        results.append({
            "name": m.name,
            "deposit": round(member_deposit, 2),
            "meals": round(member_meals, 2),
            "meal_cost": round(meal_cost, 2),
            "in_hand": round(in_hand, 2)
        })

    return {
        "total_bazar": round(total_bazar, 2),
        "total_deposit": round(total_deposit, 2),
        "total_meals": round(total_meals, 2),
        "total_meal_cost": round(total_meal_cost, 2),
        "meal_rate": round(meal_rate, 2),
        "overall_in_hand": round(overall_in_hand, 2),
        "members": results
    }



# ------------------------------
# Update Member
# ------------------------------
class MemberUpdate(BaseModel):
    name: str

@app.put("/members/{member_id}")
def update_member(member_id: int, member: MemberUpdate, db: Session = Depends(get_db)):
    db_member = db.query(models.Member).filter(models.Member.id == member_id).first()
    if not db_member:
        raise HTTPException(status_code=404, detail="Member not found")
    db_member.name = member.name
    db.commit()
    db.refresh(db_member)
    return {"message": "Member updated", "member": db_member}

# ------------------------------
# Update Deposit
# ------------------------------
class DepositUpdate(BaseModel):
    amount: float

@app.put("/deposit/{deposit_id}")
def update_deposit(deposit_id: int, deposit: DepositUpdate, db: Session = Depends(get_db)):
    db_deposit = db.query(models.Deposit).filter(models.Deposit.id == deposit_id).first()
    if not db_deposit:
        raise HTTPException(status_code=404, detail="Deposit not found")
    db_deposit.amount = deposit.amount
    db.commit()
    db.refresh(db_deposit)
    return {"message": "Deposit updated", "deposit": db_deposit}

# ------------------------------
# Update Meal
# ------------------------------
class MealUpdate(BaseModel):
    meals: float

@app.put("/meal/{meal_id}")
def update_meal(meal_id: int, meal: MealUpdate, db: Session = Depends(get_db)):
    db_meal = db.query(models.Meal).filter(models.Meal.id == meal_id).first()
    if not db_meal:
        raise HTTPException(status_code=404, detail="Meal record not found")
    db_meal.meals = meal.meals
    db.commit()
    db.refresh(db_meal)
    return {"message": "Meal updated", "meal": db_meal}

# ------------------------------
# Update Bazar
# ------------------------------
class BazarUpdate(BaseModel):
    amount: float
    description: str = ""

@app.put("/bazar/{bazar_id}")
def update_bazar(bazar_id: int, bazar: BazarUpdate, db: Session = Depends(get_db)):
    db_bazar = db.query(models.Bazar).filter(models.Bazar.id == bazar_id).first()
    if not db_bazar:
        raise HTTPException(status_code=404, detail="Bazar record not found")
    db_bazar.amount = bazar.amount
    db_bazar.description = bazar.description
    db.commit()
    db.refresh(db_bazar)
    return {"message": "Bazar record updated", "bazar": db_bazar}


# ------------------------------
# Delete single record by ID
# ------------------------------

@app.delete("/deposit/{deposit_id}")
def delete_deposit(deposit_id: int, db: Session = Depends(get_db)):
    deposit = db.query(models.Deposit).filter(models.Deposit.id == deposit_id).first()
    if not deposit:
        raise HTTPException(status_code=404, detail="Deposit not found")
    db.delete(deposit)
    db.commit()
    return {"message": f"Deposit ID {deposit_id} deleted successfully"}


@app.delete("/meal/{meal_id}")
def delete_meal(meal_id: int, db: Session = Depends(get_db)):
    meal = db.query(models.Meal).filter(models.Meal.id == meal_id).first()
    if not meal:
        raise HTTPException(status_code=404, detail="Meal not found")
    db.delete(meal)
    db.commit()
    return {"message": f"Meal ID {meal_id} deleted successfully"}


@app.delete("/bazar/{bazar_id}")
def delete_bazar(bazar_id: int, db: Session = Depends(get_db)):
    bazar = db.query(models.Bazar).filter(models.Bazar.id == bazar_id).first()
    if not bazar:
        raise HTTPException(status_code=404, detail="Bazar record not found")
    db.delete(bazar)
    db.commit()
    return {"message": f"Bazar ID {bazar_id} deleted successfully"}


@app.delete("/members/{member_id}")
def delete_member(member_id: int, db: Session = Depends(get_db)):
    member = db.query(models.Member).filter(models.Member.id == member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    # Delete related deposits, meals, bazar first (foreign key)
    db.query(models.Deposit).filter(models.Deposit.member_id == member_id).delete()
    db.query(models.Meal).filter(models.Meal.member_id == member_id).delete()
    db.query(models.Bazar).filter(models.Bazar.member_id == member_id).delete()
    db.delete(member)
    db.commit()
    return {"message": f"Member ID {member_id} and all related records deleted"}


# ------------------------------
# Clear entire table
# ------------------------------

@app.delete("/clear-table/{table_name}")
def clear_table(table_name: str, db: Session = Depends(get_db)):
    table_map = {
        "members": models.Member,
        "deposits": models.Deposit,
        "meals": models.Meal,
        "bazar": models.Bazar
    }
    if table_name not in table_map:
        raise HTTPException(status_code=400, detail="Invalid table name")
    
    db.query(table_map[table_name]).delete()
    db.commit()
    return {"message": f"All records in table '{table_name}' have been deleted"}
