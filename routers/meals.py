from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas
from database import get_db

router = APIRouter(prefix="/meal", tags=["Meals"])

@router.post("/")
def create_meal(meal: schemas.MealCreate, db: Session = Depends(get_db)):
    member = db.query(models.Member).filter(models.Member.id == meal.member_id).first()
    session = db.query(models.MealSession).filter(models.MealSession.id == meal.session_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    db_meal = models.Meal(
        member_id=meal.member_id,
        session_id=meal.session_id,
        meals=meal.meals
    )
    db.add(db_meal)
    db.commit()
    db.refresh(db_meal)
    return db_meal

@router.put("/{meal_id}")
def update_meal(meal_id: int, meal: schemas.MealUpdate, db: Session = Depends(get_db)):
    db_meal = db.query(models.Meal).filter(models.Meal.id == meal_id).first()
    if not db_meal:
        raise HTTPException(status_code=404, detail="Meal not found")
    db_meal.meals = meal.meals
    db.commit()
    db.refresh(db_meal)
    return {"message": "Meal updated", "meal": db_meal}

@router.delete("/{meal_id}")
def delete_meal(meal_id: int, db: Session = Depends(get_db)):
    meal = db.query(models.Meal).filter(models.Meal.id == meal_id).first()
    if not meal:
        raise HTTPException(status_code=404, detail="Meal not found")
    db.delete(meal)
    db.commit()
    return {"message": f"Meal ID {meal_id} deleted successfully"}
