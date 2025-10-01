from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models
from database import get_db

router = APIRouter()

@router.get("/meal-stats/{session_id}")
def meal_stats(session_id: int, db: Session = Depends(get_db)):
    session = db.query(models.MealSession).filter(models.MealSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    members = db.query(models.Member).all()

    # Total bazar for this session
    total_bazar = sum(b.amount for b in session.bazars)

    # Total deposit for this session
    total_deposit = sum(d.amount for d in session.deposits)

    # Total meals for this session
    total_meals = sum(me.meals for me in session.meals)

    # Meal rate
    meal_rate = total_bazar / total_meals if total_meals > 0 else 0
    total_meal_cost = total_meals * meal_rate

    results = []
    overall_in_hand = 0

    for m in members:
        # Filter deposits and meals by session
        member_deposit = sum(d.amount for d in m.deposits if d.session_id == session_id)
        member_meals = sum(me.meals for me in m.meals if me.session_id == session_id)

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
        "session": session.name,
        "manager": session.manager,
        "total_bazar": round(total_bazar, 2),
        "total_deposit": round(total_deposit, 2),
        "total_meals": round(total_meals, 2),
        "total_meal_cost": round(total_meal_cost, 2),
        "meal_rate": round(meal_rate, 2),
        "overall_in_hand": round(overall_in_hand, 2),
        "members": results
    }
