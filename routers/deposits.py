from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
import models, schemas
from database import get_db

router = APIRouter()

@router.post("/")
def create_deposit(deposit: schemas.DepositCreate, db: Session = Depends(get_db)):
    member = db.query(models.Member).filter(models.Member.id == deposit.member_id).first()
    session = db.query(models.MealSession).filter(models.MealSession.id == deposit.session_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    db_deposit = models.Deposit(
        member_id=deposit.member_id,
        session_id=deposit.session_id,
        amount=deposit.amount,
        date=deposit.date or date.today()
    )
    db.add(db_deposit)
    db.commit()
    db.refresh(db_deposit)
    return db_deposit

@router.put("/{deposit_id}")
def update_deposit(deposit_id: int, deposit: schemas.DepositUpdate, db: Session = Depends(get_db)):
    db_deposit = db.query(models.Deposit).filter(models.Deposit.id == deposit_id).first()
    if not db_deposit:
        raise HTTPException(status_code=404, detail="Deposit not found")
    db_deposit.amount = deposit.amount
    if deposit.date:
        db_deposit.date = deposit.date
    db.commit()
    db.refresh(db_deposit)
    return db_deposit

@router.delete("/{deposit_id}")
def delete_deposit(deposit_id: int, db: Session = Depends(get_db)):
    deposit = db.query(models.Deposit).filter(models.Deposit.id == deposit_id).first()
    if not deposit:
        raise HTTPException(status_code=404, detail="Deposit not found")
    db.delete(deposit)
    db.commit()
    return {"message": f"Deposit ID {deposit_id} deleted successfully"}
