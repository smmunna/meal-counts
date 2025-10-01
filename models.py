from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Member(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    deposits = relationship("Deposit", back_populates="member")
    meals = relationship("Meal", back_populates="member")
    bazars = relationship("Bazar", back_populates="member", cascade="all, delete-orphan")  # string name works

class Deposit(Base):
    __tablename__ = "deposits"

    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, ForeignKey("members.id"))
    amount = Column(Float)

    member = relationship("Member", back_populates="deposits")


class Meal(Base):
    __tablename__ = "meals"

    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, ForeignKey("members.id"))
    meals = Column(Float)

    member = relationship("Member", back_populates="meals")

class Bazar(Base):
    __tablename__ = "bazar"

    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, ForeignKey("members.id"))
    amount = Column(Float)
    description = Column(String, default="")

    member = relationship("Member", back_populates="bazars")  # <-- fix here
