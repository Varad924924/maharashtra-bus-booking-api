from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import buses, bookings
from app.database import engine
from app import models
from app.routers import buses, bookings, auth  # <-- Add auth here!



# --- THIS COMMAND CREATES THE DATABASE FILE AUTOMATICALLY ---
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Bus Booking System")

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