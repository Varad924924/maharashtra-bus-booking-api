from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default="user")  # Can be 'user' or 'admin'
    created_at = Column(DateTime, default=datetime.utcnow)

    # A user can have many bookings
    bookings = relationship("Booking", back_populates="user", cascade="all, delete-orphan")


class Bus(Base):
    __tablename__ = "buses"

    id = Column(Integer, primary_key=True, index=True)
    bus_number = Column(String, unique=True, index=True)
    operator = Column(String)
    source = Column(String)
    destination = Column(String)
    date = Column(String)
    departure_time = Column(String)
    total_seats = Column(Integer, default=40)
    price = Column(Float)

    bookings = relationship("Booking", back_populates="bus", cascade="all, delete-orphan")


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    bus_id = Column(Integer, ForeignKey("buses.id"))
    user_id = Column(Integer, ForeignKey("users.id"))  # <--- NEW: Links to User

    passenger_name = Column(String)
    age = Column(Integer)
    gender = Column(String)
    seat_number = Column(Integer)
    mobile_no = Column(String)
    adhaar_no = Column(String)
    payment_mode = Column(String)
    total_amount = Column(Float)

    # Relationships
    bus = relationship("Bus", back_populates="bookings")
    user = relationship("User", back_populates="bookings")  # <--- NEW