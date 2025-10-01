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
