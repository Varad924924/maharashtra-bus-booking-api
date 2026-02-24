from pydantic import BaseModel
from typing import Optional
import re
from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

    @field_validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if not re.search(r"[A-Z]", v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r"[a-z]", v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r"\d", v):
            raise ValueError('Password must contain at least one digit')
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
            raise ValueError('Password must contain at least one special character')
        return v

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str

    class Config:
        from_attributes = True

# --- BUS SCHEMAS ---
class BusBase(BaseModel):
    bus_number: str
    operator: str
    source: str
    destination: str
    date: str          # NEW
    departure_time: str
    total_seats: int
    price: float

class BusCreate(BusBase):
    pass

class BusResponse(BusBase):
    id: int
    class Config:
        from_attributes = True

# SCENARIO 1: Search now includes DATE
class BusSearch(BaseModel):
    source: str
    destination: str
    date: str  # Format: "2025-02-10"

# --- BOOKING SCHEMAS ---
# SCENARIO 2 & 3: Passenger Info + Payment
class BookingCreate(BaseModel):
    bus_id: int
    passenger_name: str
    age: int
    gender: str
    adhaar_no: str
    mobile_no: str
    seat_number: int
    payment_mode: str  # "Cash" or "Online"

class BookingResponse(BookingCreate):
    id: int
    total_amount: float
    class Config:
        from_attributes = True