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

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./mess.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# ✅ This is important
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
