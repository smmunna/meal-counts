from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas
from database import get_db

router = APIRouter(prefix="/sessions", tags=["Sessions"])

@router.post("/")
def create_session(session: schemas.SessionCreate, db: Session = Depends(get_db)):
    db_session = models.MealSession(
        name=session.name,
        manager=session.manager,
        start_date=session.start_date,
        end_date=session.end_date
    )
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session

@router.get("/")
def get_sessions(db: Session = Depends(get_db)):
    return db.query(models.MealSession).all()
