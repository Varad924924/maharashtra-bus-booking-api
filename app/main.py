from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import buses, bookings
from app.database import engine
from app import models
from app.routers import buses, bookings, auth  # <-- Add auth here!





# --- THIS COMMAND CREATES THE DATABASE FILE AUTOMATICALLY ---
models.Base.metadata.create_all(bind=engine)

tags_metadata = [
    {
        "name": "Authentication",
        "description": "Operations with users. The **login** logic is here.",
    },
    {
        "name": "Buses",
        "description": "Manage buses. Look up buses, as well as functions to add, update, and delete them (Admin only).",
    },
    {
        "name": "Bookings",
        "description": "Manage user bookings and retrieve taken seats for buses.",
    },
]

app = FastAPI(
    title="Maharashtra Bus Booking System API",
    description="API Documentation for the Maharashtra Bus Booking System. Manage buses, make reservations, and handle user authentication easily via these documented endpoints.",
    version="1.0.0",
    contact={
        "name": "Varad Gorhe",
        "email": "varadgorhe2019@gmail.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    openapi_tags=tags_metadata
)

from app.database import SessionLocal
from app.models import User
from passlib.context import CryptContext

# 1. Set up the password hasher (bcrypt)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@app.on_event("startup")
def auto_create_admin():
    db = SessionLocal()
    try:
        admin_email = "varadgorhe2019@gmail.com"

        # 2. Check if the database was wiped
        existing_admin = db.query(User).filter(User.email == admin_email).first()

        # 3. If wiped, rebuild it with a HASHED password!
        if not existing_admin:
            # Pick the password you want to type on the login screen
            plain_text_password = "Varad@924"

            # Hash it securely
            safe_hashed_password = pwd_context.hash(plain_text_password)

            new_admin = User(
                name="Varad Gorhe",
                email=admin_email,
                password=safe_hashed_password,  # Safely stored!
                role="admin"
            )
            db.add(new_admin)
            db.commit()
            print(f"🤖 AUTO-SEED: Admin {admin_email} created with a secure password!")
    except Exception as e:
        print(f"Auto-seed error: {e}")
    finally:
        db.close()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # <--- This "*" allows your file:///C:/... to connect
    allow_credentials=True,
    allow_methods=["*"],  # Allows POST, GET, PUT, DELETE
    allow_headers=["*"],
)


app.include_router(auth.router)
app.include_router(buses.router, prefix="/buses", tags=["Buses"])
app.include_router(bookings.router, prefix="/bookings", tags=["Bookings"])

from datetime import datetime, timedelta
import random
from app.models import Bus  # Make sure your Bus model is imported!
from fastapi import Depends
from app.database import get_db
from sqlalchemy.orm import Session


@app.post("/buses/auto-generate")
def auto_generate_buses(db: Session = Depends(get_db)):
    # 1. Define your cities and fake operators
    routes = [
        ("Pune", "Mumbai"), ("Mumbai", "Pune"),
        ("Pune", "Nashik"), ("Nashik", "Pune"),
        ("Pune", "A.Nagar"), ("A.Nagar", "Pune"),
        ("Mumbai", "Nashik"), ("Nashik", "Mumbai")
    ]
    operators = ["Maharashtra Travels", "Shivneri Express", "VRL Travels", "Neeta Volvo"]

    # 2. Start from exactly right now
    start_time = datetime.now()
    generated_count = 0

    # 3. Loop for the next 24 hours
    for hour_offset in range(24):
        current_time = start_time + timedelta(hours=hour_offset)
        date_str = current_time.strftime("%Y-%m-%d")
        time_str = current_time.strftime("%H:%M")

        # Pick 3 random routes to run every single hour
        hourly_routes = random.sample(routes, 3)

        for source, destination in hourly_routes:
            new_bus = Bus(
                bus_number=f"MH-{random.randint(11, 40)}-{random.randint(1000, 9999)}",
                operator=random.choice(operators),
                source=source,
                destination=destination,
                date=date_str,
                departure_time=time_str,
                total_seats=40,
                price=random.choice([450, 600, 750, 900])
            )
            db.add(new_bus)
            generated_count += 1

    # 4. Save all to the database at once!
    db.commit()
    return {"message": f"⚡ SUCCESS! {generated_count} new buses generated for the next 24 hours!"}

@app.get("/")
def home():
    return {"message": "Welcome to the Bus Booking API"}


from app.database import SessionLocal
from app.models import User

@app.get("/upgrade-admin/{email}")
def upgrade_admin(email: str):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()
        if user:
            user.role = "admin"
            db.commit()
            return {"message": f"🎉 SUCCESS! {email} is now an ADMIN!"}
        return {"error": "User not found. Make sure you signed up on the frontend first!"}
    finally:
        db.close()


from app.models import User


@app.get("/users/")
def get_all_users(db: Session = Depends(get_db)):
    # Fetch all users from the database
    users = db.query(User).all()

    # Return a safe list without the hashed passwords!
    safe_users = []
    for u in users:
        safe_users.append({
            "id": u.id,
            "name": u.name,
            "email": u.email,
            "role": u.role
        })

    return safe_users