from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import Base, engine, get_db
import models
from routers import members, deposits, meals, bazars, sessions, stats


# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Meal Management with Daily Tracking")

# Include routers
app.include_router(sessions.router, prefix="/sessions", tags=["Sessions"])
app.include_router(members.router, prefix="/members", tags=["Members"])
app.include_router(deposits.router, prefix="/deposits", tags=["Deposits"])
app.include_router(meals.router, prefix="/meals", tags=["Meals"])
app.include_router(bazars.router, prefix="/bazar", tags=["Bazar"])
app.include_router(stats.router, prefix="/stats", tags=["Stats"])




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
