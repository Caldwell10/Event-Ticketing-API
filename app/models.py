from .database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func, Index, CheckConstraint,text
from sqlalchemy.orm import relationship

# Define User model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String,nullable=False)

    reservations = relationship("Reservation", back_populates="user")

# Define Shows model
class Show(Base):
    __tablename__ = "shows"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    venue = Column(String, nullable=False, index=True)
    starts_at = Column(DateTime(timezone=True), nullable=False, index=True)

    seats = relationship("Seat", back_populates="show", cascade="all, delete-orphan") 

# Define Seats model
class Seat(Base):
    __tablename__ = "seats"

    id = Column(Integer, primary_key=True, index=True)
    seat_number = Column(String, index=True, nullable=False)
    show_id = Column(Integer, ForeignKey("shows.id", ondelete="CASCADE"), nullable=False)

    show = relationship("Show", back_populates="seats")
    reservations=relationship("Reservation", back_populates="seat", cascade="all, delete-orphan")

    # prevent duplicate labels within the show e.g  two A2 seats in the same show
    __table_args__ = (
        Index("unique_label_per_show", "show_id", "seat_number", unique=True),
    )


# Define Reservations model
class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    seat_id = Column(Integer, ForeignKey("seats.id", ondelete="CASCADE"), nullable=False, index=True)
    status = Column(String, server_default="HELD", nullable=False)  # expiry logic
    hold_expiry = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False) 

    
    user = relationship("User", back_populates="reservations")
    seat = relationship("Seat", back_populates="reservations")
    

    __table_args__ = (
        # one active reservation (HELD or CONFIRMED) per seat
        Index('unique_active_reservation_per_seat',
            'seat_id',
            unique=True,
            postgresql_where = text("status IN ('HELD', 'CONFIRMED')")
        ),
        CheckConstraint(
            "status IN ('HELD', 'CONFIRMED', 'EXPIRED')",
            name = "reservation_status_check"
        )
    )









    