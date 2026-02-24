import requests
import datetime

# Login first
LOGIN_URL = "http://127.0.0.1:8000/auth/login"
API_URL = "http://127.0.0.1:8000/buses/"
token = requests.post(LOGIN_URL, data={"username": "admin", "password": "secret123"}).json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}

# Get Today's Date (e.g., "2025-02-06")
today = datetime.date.today().strftime("%Y-%m-%d")
tomorrow = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")

buses = [
    # Buses for TODAY
    {"bus_number": "MH-14-1001", "operator": "Shivneri", "source": "Pune", "destination": "Mumbai", "date": today,
     "departure_time": "08:00 AM", "total_seats": 40, "price": 450.0},
    {"bus_number": "MH-14-1002", "operator": "Neeta", "source": "Pune", "destination": "Mumbai", "date": today,
     "departure_time": "10:00 AM", "total_seats": 40, "price": 500.0},

    # Buses for TOMORROW
    {"bus_number": "MH-14-1003", "operator": "Shivneri", "source": "Pune", "destination": "Mumbai", "date": tomorrow,
     "departure_time": "08:00 AM", "total_seats": 40, "price": 450.0},
]

for bus in buses:
    requests.post(API_URL, json=bus, headers=headers)

print(f"✅ Added buses for {today} and {tomorrow}!")