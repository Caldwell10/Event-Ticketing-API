from database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Date, Time, func
from sqlalchemy.orm import relationship
from datetime import datetime, time, date



class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String,nullable=False)
    is_active = Column(Boolean, default=True)

    reservations = relationship("Reservations", back_populates="user", cascade="all, delete-orphan")


class Shows(Base):
    __tablename__ = "shows"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    venue = Column(String, nullable=False, index=True)
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)

    seats = relationship("Seats", back_populates="shows", cascade="all, delete-orphan") 

class Seats(Base):
    __tablename__ = "seats"

    id = Column(Integer, primary_key=True, index=True)
    seat_number = Column(String, unique=True, index=True, nullable=False)
    is_available = Column(Boolean, default=True)

    shows = relationship("Shows", back_populates="seats")

class Reservations(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    seat_id = Column(Integer, ForeignKey("seats.id"), nullable=False)
    show_id = Column(Integer, ForeignKey("shows.id"), nullable=False)
    reservation_time = Column(DateTime, server_default=func.now())
    status = Column(String, server_default="AVAILABLE")  # e.g., active, cancelled

    user = relationship("User", back_populates="reservations")
    seat = relationship("Seats")
    show = relationship("Shows")

    __table_args__ = (
        # Ensure that 
    )









    