import requests
import json

# The URL where your server accepts new buses
url = "http://127.0.0.1:8000/buses/"

print("--- Starting to Add 24 Buses ---")

# Loop from 1 to 24 to create buses for every hour
for i in range(1, 25):
    # Create the bus number (e.g., 1001, 1002...)
    bus_num = 1000 + i

    # Format time (e.g., "01:00 AM", "13:00 PM")
    time_label = "AM" if i < 12 else "PM"
    display_hour = i if i <= 12 else i - 12
    formatted_time = f"{display_hour:02d}:00 {time_label}"

    # The Data for ONE bus
    payload = {
        "bus_number": f"MH-12-PM-{bus_num}",
        "operator": "Shivneri",
        "source": "Pune",
        "destination": "Mumbai",
        "departure_time": formatted_time,
        "total_seats": 40,
        "price": 500.0
    }

    # Send it to the server
    response = requests.post(url, json=payload)

    if response.status_code == 200:
        print(f"✅ Added: {payload['bus_number']} at {formatted_time}")
    else:
        print(f"❌ Failed: {response.text}")

print("--- Done! ---")