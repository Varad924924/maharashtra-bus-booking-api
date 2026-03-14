from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from datetime import datetime
from app import models, schemas, database
from app.routers import auth

router = APIRouter()


def get_db():
    return next(database.get_db())


# --- HELPER: DELETE OLD BUSES ---
def delete_expired_buses(db: Session):
    """
    Checks all buses. If their Date + Time is in the past, delete them.
    """
    all_buses = db.query(models.Bus).all()
    current_time = datetime.now()

    for bus in all_buses:
        try:
            # Combine Date and Time strings into a single datetime object
            # Format matches: "2026-02-06" + " " + "08:00 AM"
            bus_datetime_str = f"{bus.date} {bus.departure_time}"
            bus_dt = datetime.strptime(bus_datetime_str, "%Y-%m-%d %I:%M %p")

            # If the bus time is older than NOW, delete it
            if bus_dt < current_time:
                db.delete(bus)

        except ValueError:
            # If time format is wrong, ignore it (safety check)
            continue

    # Save the deletions
    db.commit()


# --- ROUTES ---

@router.get("/", response_model=List[schemas.BusResponse], summary="List all active buses", description="Retrieves a list of all active buses. Past/expired buses are automatically cleaned up before returning.")
def get_buses(db: Session = Depends(get_db)):
    delete_expired_buses(db)  # <--- Clean up before showing list
    return db.query(models.Bus).all()


@router.post("/search", response_model=List[schemas.BusResponse], summary="Search available buses", description="Searches for active buses matching the specified source, destination, and date (case-insensitive).")
def search_buses(search_data: schemas.BusSearch, db: Session = Depends(get_db)):
    delete_expired_buses(db)  # <--- Clean up before searching

    # Standard Search Logic (Case Insensitive)
    results = db.query(models.Bus).filter(
        func.lower(models.Bus.source) == search_data.source.lower(),
        func.lower(models.Bus.destination) == search_data.destination.lower(),
        models.Bus.date == search_data.date
    ).all()

    if not results:
        return []
    return results


# --- ADMIN ROUTES ---
@router.post("/", response_model=schemas.BusResponse, dependencies=[Depends(auth.get_admin_user)], summary="Add a new bus", description="**Admin Only:** Adds a new bus schedule to the system.")
def add_bus(bus: schemas.BusCreate, db: Session = Depends(get_db)):
    new_bus = models.Bus(**bus.dict())
    db.add(new_bus)
    db.commit()
    db.refresh(new_bus)
    return new_bus


@router.delete("/{bus_id}", dependencies=[Depends(auth.get_admin_user)], summary="Delete a bus", description="**Admin Only:** Permanently removes a bus from the system by ID.")
def delete_bus(bus_id: int, db: Session = Depends(get_db)):
    bus = db.query(models.Bus).filter(models.Bus.id == bus_id).first()
    if not bus:
        raise HTTPException(status_code=404, detail="Bus not found")
    db.delete(bus)
    db.commit()
    return {"message": "Bus deleted successfully"}


@router.put("/{bus_id}", response_model=schemas.BusResponse, dependencies=[Depends(auth.get_admin_user)], summary="Update bus details", description="**Admin Only:** Updates the details of an existing bus by ID.")
def update_bus(bus_id: int, bus_update: schemas.BusCreate, db: Session = Depends(get_db)):
    bus = db.query(models.Bus).filter(models.Bus.id == bus_id).first()
    if not bus:
        raise HTTPException(status_code=404, detail="Bus not found")

    # Update all the fields
    for key, value in bus_update.dict().items():
        setattr(bus, key, value)

    db.commit()
    db.refresh(bus)
    return bus