import requests

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

# Extract the token
token = login_response.json()["access_token"]
print("✅ Login Success! Token received.")

# 2. Prepare the Header with the Token
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# 3. List of Buses to Add
buses = []
for i in range(1, 25):  # 24 Buses
    hour = i % 12
    if hour == 0: hour = 12
    ampm = "AM" if i < 12 else "PM"
    time = f"{hour:02d}:00 {ampm}"

    buses.append({
        "bus_number": f"MH-12-NP{1000 + i}",
        "operator": "Shivneri",
        "source": "Nashik",
        "destination": "Pune",
        "departure_time": time,
        "total_seats": 40,
        "price": 500.0
    })

# 4. Add Buses using the Token
print("--- Starting to Add Buses ---")
for bus in buses:
    response = requests.post(API_URL, json=bus, headers=headers)  # <--- Sending Token Here
    if response.status_code == 200:
        print(f"✅ Added: {bus['bus_number']}")
    else:
        print(f"❌ Failed: {response.text}")

print("--- Done! ---")