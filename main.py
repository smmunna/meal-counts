from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import Base, engine, get_db
import models
from routers import members, deposits, meals, bazars

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Meal Management API")

# Routers
app.include_router(members.router)
app.include_router(deposits.router)
app.include_router(meals.router)
app.include_router(bazars.router)

# ------------------------------
# Meal Stats
# ------------------------------
@app.get("/meal-stats/")
def meal_stats(db: Session = Depends(get_db)):
    members = db.query(models.Member).all()
    total_bazar = sum(b.amount for b in db.query(models.Bazar).all())
    total_deposit = sum(d.amount for d in db.query(models.Deposit).all())
    total_meals = sum(sum(me.meals for me in m.meals) for m in members)

    meal_rate = total_bazar / total_meals if total_meals > 0 else 0
    total_meal_cost = total_meals * meal_rate

    results, overall_in_hand = [], 0
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
    return {"message": f"All records in table '{table_name}' deleted"}


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
