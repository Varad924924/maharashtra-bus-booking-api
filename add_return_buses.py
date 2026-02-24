import requests
import datetime

# 1. Login to get the Token
LOGIN_URL = "http://127.0.0.1:8000/auth/login"
API_URL = "http://127.0.0.1:8000/buses/"

login_data = {
    "username": "admin",
    "password": "secret123"
}

print("🔐 Logging in as Admin...")
login_response = requests.post(LOGIN_URL, data=login_data)

if login_response.status_code != 200:
    print("❌ Login Failed! Check username/password.")
    exit()

token = login_response.json()["access_token"]
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# 2. Calculate Dates (Today & Tomorrow)
today = datetime.date.today().strftime("%Y-%m-%d")
tomorrow = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
dates_to_add = [today, tomorrow]

print(f"📅 Adding buses for: {dates_to_add}")

# 3. List of Buses to Add (Nashik -> Pune)
buses = []

for date in dates_to_add:
    for i in range(1, 13):  # Let's add 12 buses per day
        # Calculate Time
        hour = 6 + i  # Start from 7 AM
        if hour > 12:
            hour_display = hour - 12
        else:
            hour_display = hour

        ampm = "AM" if hour < 12 else "PM"
        time_str = f"{hour_display:02d}:00 {ampm}"

        buses.append({
            "bus_number": f"MH-15-NP-{100 + i}",  # MH-15 is Nashik code
            "operator": "Shivneri",
            "source": "Nashik",  # <--- Source
            "destination": "Pune",  # <--- Destination
            "date": date,  # <--- CRITICAL NEW FIELD
            "departure_time": time_str,
            "total_seats": 40,
            "price": 450.0
        })

# 4. Send to API
print(f"--- Starting to Add {len(buses)} Buses ---")
for bus in buses:
    response = requests.post(API_URL, json=bus, headers=headers)
    if response.status_code == 200:
        print(f"✅ Added: {bus['bus_number']} ({bus['date']} @ {bus['departure_time']})")
    else:
        print(f"❌ Failed: {response.text}")

print("--- Done! ---")