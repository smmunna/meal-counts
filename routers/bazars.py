from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas
from database import get_db

router = APIRouter(prefix="/bazar", tags=["Bazar"])

@router.post("/")
def add_bazar(bazar: schemas.BazarCreate, db: Session = Depends(get_db)):
    member = db.query(models.Member).filter(models.Member.id == bazar.member_id).first()
    session = db.query(models.MealSession).filter(models.MealSession.id == bazar.session_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    db_bazar = models.Bazar(
        member_id=bazar.member_id,
        session_id=bazar.session_id,
        amount=bazar.amount,
        description=bazar.description
    )
    db.add(db_bazar)
    db.commit()
    db.refresh(db_bazar)
    return db_bazar

@router.put("/{bazar_id}")
def update_bazar(bazar_id: int, bazar: schemas.BazarUpdate, db: Session = Depends(get_db)):
    db_bazar = db.query(models.Bazar).filter(models.Bazar.id == bazar_id).first()
    if not db_bazar:
        raise HTTPException(status_code=404, detail="Bazar not found")
    db_bazar.amount = bazar.amount
    db_bazar.description = bazar.description
    db.commit()
    db.refresh(db_bazar)
    return {"message": "Bazar updated", "bazar": db_bazar}

@router.delete("/{bazar_id}")
def delete_bazar(bazar_id: int, db: Session = Depends(get_db)):
    bazar = db.query(models.Bazar).filter(models.Bazar.id == bazar_id).first()
    if not bazar:
        raise HTTPException(status_code=404, detail="Bazar not found")
    db.delete(bazar)
    db.commit()
    return {"message": f"Bazar ID {bazar_id} deleted successfully"}
