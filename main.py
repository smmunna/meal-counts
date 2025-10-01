from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import Base, engine, get_db
import models
from routers import members, deposits, meals, bazars, sessions

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Meal Management with Sessions")

# Include routers
app.include_router(members.router)
app.include_router(deposits.router)
app.include_router(meals.router)
app.include_router(bazars.router)
app.include_router(sessions.router)

# ------------------------------
# Meal Stats per Session
# ------------------------------
@app.get("/stats/meal-stats/{session_id}")
def meal_stats(session_id: int, db: Session = Depends(get_db)):
    members = db.query(models.Member).all()
    session = db.query(models.MealSession).filter(models.MealSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    total_bazar = sum(b.amount for b in session.bazars)
    total_deposit = sum(d.amount for d in session.deposits)
    total_meals = sum(sum(me.meals for me in m.meals if me.session_id==session_id) for m in members)
    meal_rate = total_bazar / total_meals if total_meals > 0 else 0
    total_meal_cost = total_meals * meal_rate

    results, overall_in_hand = [], 0
    for m in members:
        member_deposit = sum(d.amount for d in m.deposits if d.session_id==session_id)
        member_meals = sum(me.meals for me in m.meals if me.session_id==session_id)
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

# ------------------------------
# Clear entire table
# ------------------------------
@app.delete("/clear-table/{table_name}")
def clear_table(
    table_name: str,
    session_id: int = Query(None, description="Optional: ID of session to clear"),
    db: Session = Depends(get_db)
):
    table_map = {
        "members": models.Member,
        "deposits": models.Deposit,
        "meals": models.Meal,
        "bazar": models.Bazar
    }
    if table_name not in table_map:
        raise HTTPException(status_code=400, detail="Invalid table name")
    
    Model = table_map[table_name]

    if session_id and table_name in ["deposits", "meals", "bazar"]:
        # Only delete records for the given session
        deleted_count = db.query(Model).filter(Model.session_id == session_id).delete()
    elif session_id and table_name == "members":
        raise HTTPException(status_code=400, detail="Cannot clear members by session")
    else:
        # Delete all records in table
        deleted_count = db.query(Model).delete()
    
    db.commit()
    return {
        "message": f"Deleted {deleted_count} records from table '{table_name}'"
        + (f" for session ID {session_id}" if session_id else "")
    }
