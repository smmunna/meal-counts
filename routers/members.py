from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas
from database import get_db

router = APIRouter(prefix="/members", tags=["Members"])

@router.post("/")
def create_member(member: schemas.MemberCreate, db: Session = Depends(get_db)):
    db_member = models.Member(name=member.name)
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member

@router.put("/{member_id}")
def update_member(member_id: int, member: schemas.MemberUpdate, db: Session = Depends(get_db)):
    db_member = db.query(models.Member).filter(models.Member.id == member_id).first()
    if not db_member:
        raise HTTPException(status_code=404, detail="Member not found")
    db_member.name = member.name
    db.commit()
    db.refresh(db_member)
    return {"message": "Member updated", "member": db_member}

@router.delete("/{member_id}")
def delete_member(member_id: int, db: Session = Depends(get_db)):
    member = db.query(models.Member).filter(models.Member.id == member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    db.delete(member)
    db.commit()
    return {"message": f"Member ID {member_id} and all related records deleted"}
