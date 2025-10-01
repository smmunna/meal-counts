from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import relationship
from database import Base
from datetime import date

class Member(Base):
    __tablename__ = "members"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    deposits = relationship("Deposit", back_populates="member", cascade="all, delete")
    meals = relationship("Meal", back_populates="member", cascade="all, delete")
    bazars = relationship("Bazar", back_populates="member", cascade="all, delete")


class MealSession(Base):
    __tablename__ = "sessions"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    manager = Column(String, nullable=True)
    start_date = Column(Date)
    end_date = Column(Date, nullable=True)

    deposits = relationship("Deposit", back_populates="session")
    meals = relationship("Meal", back_populates="session")
    bazars = relationship("Bazar", back_populates="session")


class Deposit(Base):
    __tablename__ = "deposits"
    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, ForeignKey("members.id"))
    session_id = Column(Integer, ForeignKey("sessions.id"))
    amount = Column(Float)
    date = Column(Date, default=date.today)

    member = relationship("Member", back_populates="deposits")
    session = relationship("MealSession", back_populates="deposits")


class Meal(Base):
    __tablename__ = "meals"
    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, ForeignKey("members.id"))
    session_id = Column(Integer, ForeignKey("sessions.id"))
    meals = Column(Float)
    date = Column(Date, default=date.today)

    member = relationship("Member", back_populates="meals")
    session = relationship("MealSession", back_populates="meals")


class Bazar(Base):
    __tablename__ = "bazar"
    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, ForeignKey("members.id"))
    session_id = Column(Integer, ForeignKey("sessions.id"))
    amount = Column(Float)
    description = Column(String, default="")
    date = Column(Date, default=date.today)

    member = relationship("Member", back_populates="bazars")
    session = relationship("MealSession", back_populates="bazars")
