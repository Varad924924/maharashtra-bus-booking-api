from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas, database
from app.routers import auth  # <-- We import your new auth system!

router = APIRouter()

def get_db():
    return next(database.get_db())

# ==========================================
# 1. CREATE BOOKING (REQUIRES USER LOGIN)
# ==========================================
@router.post("/", response_model=schemas.BookingResponse, summary="Create a new booking", description="Creates a booking for a specific seat on a bus. Automatically assigns the booking to the currently logged-in user.")
def create_booking(booking: schemas.BookingCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    # 1. Find the Bus
    bus = db.query(models.Bus).filter(models.Bus.id == booking.bus_id).first()
    if not bus:
        raise HTTPException(status_code=404, detail="Bus not found")

    # 2. Check if seat is already taken
    existing_booking = db.query(models.Booking).filter(
        models.Booking.bus_id == booking.bus_id,
        models.Booking.seat_number == booking.seat_number
    ).first()

    if existing_booking:
        raise HTTPException(status_code=400, detail="Seat already booked!")

    # 3. Save Booking & Link it to the Logged-in User!
    new_booking = models.Booking(
        **booking.dict(),
        total_amount=bus.price,
        user_id=current_user.id  # <-- Magic happens here!
    )

    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)

    return new_booking

# ==========================================
# 2. VIEW ALL BOOKINGS (ADMIN ONLY!)
# ==========================================
@router.get("/", response_model=List[schemas.BookingResponse], dependencies=[Depends(auth.get_admin_user)], summary="Get all bookings", description="**Admin Only:** Fetches every ticket in the system.")
def get_all_bookings(db: Session = Depends(get_db)):
    """Fetches every ticket in the system. Only Admins can do this."""
    return db.query(models.Booking).all()

# ==========================================
# 3. VIEW MY BOOKINGS (FOR REGULAR USERS)
# ==========================================
@router.get("/my-bookings", response_model=List[schemas.BookingResponse], summary="Get my active bookings", description="Fetches all tickets that belong to the logged-in user.")
def get_my_bookings(db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    """Fetches only the tickets that belong to the logged-in user."""
    return db.query(models.Booking).filter(models.Booking.user_id == current_user.id).all()

# ==========================================
# 4. GET BOOKED SEATS FOR A SPECIFIC BUS
# ==========================================
@router.get("/bus/{bus_id}", response_model=List[int], summary="Get taken seats for a bus", description="Public route to get a list of occupied seat numbers for a specific bus ID.")
def get_booked_seats(bus_id: int, db: Session = Depends(get_db)):
    """Public route so the frontend grid knows which seats to color red."""
    bookings = db.query(models.Booking).filter(models.Booking.bus_id == bus_id).all()
    return [booking.seat_number for booking in bookings]