from datetime import datetime, timedelta
from app.database import SessionLocal
from app.models import Bus


def generate_24hr_buses():
    # Open a connection to your database
    db = SessionLocal()

    try:
        # Get the current time and start from the next full hour
        now = datetime.now()
        start_time = now.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)

        # Route Information
        source = "Pune"
        destination = "Nashik"
        operator = "Shivneri"
        total_seats = 40
        price = 650.0

        buses_to_add = []

        # Loop 24 times to create 24 buses
        for i in range(24):
            # Add exactly 'i' hours to the start time
            schedule_time = start_time + timedelta(hours=i)

            # Format the date and time exactly how your database expects them
            bus_date = schedule_time.strftime("%Y-%m-%d")
            bus_time = schedule_time.strftime("%I:%M %p")  # e.g., '02:00 PM'

            # Create a unique bus number (e.g., MH-12-AUTO-100)
            bus_number = f"MH-12-AB-{1000 + i}"

            # Create the Bus Database Object
            new_bus = Bus(
                bus_number=bus_number,
                operator=operator,
                source=source,
                destination=destination,
                date=bus_date,
                departure_time=bus_time,
                total_seats=total_seats,
                price=price
            )
            buses_to_add.append(new_bus)

        # Bulk insert all 24 buses into the database at once!
        db.add_all(buses_to_add)
        db.commit()

        print("🎉 SUCCESS! 24 Buses added to the database.")
        print(f"🚍 First Bus: {buses_to_add[0].date} at {buses_to_add[0].departure_time}")
        print(f"🚍 Last Bus:  {buses_to_add[-1].date} at {buses_to_add[-1].departure_time}")

    except Exception as e:
        print(f"❌ Error adding buses: {e}")
        db.rollback()
    finally:
        # Always close the database connection
        db.close()


if __name__ == "__main__":
    print("Running bus automation script...")
    generate_24hr_buses()