"""
Meal Counts App (FastAPI)

Developer: Minhazul Abedin Munna
GitHub: https://github.com/smmunna
LinkedIn: https://www.linkedin.com/in/minhazulabedinmunna/

Description:
This FastAPI project manages meal counts, daily deposits, bazar expenses, and session-wise monthly reports.
All operations are date-wise and session-wise to ensure historical data integrity.

Project Structure:
- main.py        : FastAPI entry point
- database.py    : Database connection and setup
- models.py      : SQLAlchemy models
- schemas.py     : Pydantic schemas
- routers/       : Separate route modules for members, deposits, meals, bazars, sessions
"""


from fastapi import APIRouter, HTTPException
from database import engine
from models import Base

router = APIRouter()

@router.delete("/reset-database/")
def reset_database():
    """
    WARNING: This will DELETE all existing data in the database.
    It drops all tables and recreates them.
    """
    try:
        Base.metadata.drop_all(bind=engine)      # Drop all tables
        Base.metadata.create_all(bind=engine)    # Recreate tables
        return {"message": "Database reset successfully. All data deleted!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error resetting database: {str(e)}")
