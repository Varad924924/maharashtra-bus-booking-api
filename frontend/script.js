const API_URL = "http://192.168.1.37:8000";

// --- 1. AUTHENTICATION CHECK ---
const token = localStorage.getItem('token');
const userName = localStorage.getItem('user_name');

if (!token) {
    window.location.href = "login.html";
}

document.addEventListener("DOMContentLoaded", () => {
    document.getElementById('user-greeting').innerText = `Welcome, ${userName}!`;
});

function logout() {
    localStorage.clear();
    window.location.href = "login.html";
}

function viewMyBookings() {
    window.location.href = "my_bookings.html";
}

// --- 2. SEARCH BUSES ---
async function searchBuses() {
    const searchData = {
        source: document.getElementById('source').value,
        destination: document.getElementById('destination').value,
        date: document.getElementById('date').value
    };

    try {
        const response = await fetch(`${API_URL}/buses/search`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(searchData)
        });

        const buses = await response.json();
        const busList = document.getElementById('bus-list');
        busList.innerHTML = '';

        document.getElementById('results-card').style.display = 'block';
        document.getElementById('booking-section').style.display = 'none';

        if (buses.length === 0) {
            busList.innerHTML = '<p style="color: var(--admin-red);">No buses found for this route and date.</p>';
            return;
        }

        buses.forEach(bus => {
            const div = document.createElement('div');
            div.className = 'bus-card';
            div.innerHTML = `
                <div>
                    <h3 style="color: var(--primary); margin-bottom: 5px;">${bus.operator}</h3>
                    <p style="margin: 0; color: var(--text-muted);">${bus.departure_time} | ₹${bus.price}</p>
                </div>
                <button onclick="selectBus(${bus.id}, '${bus.operator}', ${bus.price})" style="width: auto; padding: 8px 15px;">Select Seats</button>
            `;
            busList.appendChild(div);
        });
    } catch (error) {
        console.error("Search error:", error);
    }
}

// --- 3. SEAT SELECTION ---
let currentBusPrice = 0;

async function selectBus(busId, operatorName, price) {
    document.getElementById('booking-section').style.display = 'block';
    document.getElementById('selected-bus-info').innerText = `${operatorName} (Bus #${busId})`;
    document.getElementById('book-bus-id').value = busId;
    document.getElementById('display-price').innerText = price;
    document.getElementById('booking-form').style.display = 'none';
    currentBusPrice = price;

    try {
        // Fetch which seats are already taken!
        const response = await fetch(`${API_URL}/bookings/bus/${busId}`);
        const bookedSeats = await response.json();

        const seatMap = document.getElementById('seat-map');
        seatMap.innerHTML = '';

        // Generate 40 seats
        for (let i = 1; i <= 40; i++) {
            const seat = document.createElement('div');
            seat.className = 'seat';
            seat.innerText = i;

            if (bookedSeats.includes(i)) {
                seat.classList.add('booked');
            } else {
                seat.onclick = () => selectSeat(seat, i);
            }
            seatMap.appendChild(seat);
        }
    } catch (error) {
        console.error("Seat fetch error:", error);
    }
}

function selectSeat(seatElement, seatNumber) {
    // Deselect previously selected seat
    document.querySelectorAll('.seat.selected').forEach(s => s.classList.remove('selected'));

    // Select new seat
    seatElement.classList.add('selected');
    document.getElementById('book-seat-number').value = seatNumber;

    // Show the booking form
    document.getElementById('booking-form').style.display = 'block';
}

// --- 4. SUBMIT BOOKING (WITH TOKEN) ---
document.getElementById('booking-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const bookingData = {
        bus_id: parseInt(document.getElementById('book-bus-id').value),
        passenger_name: document.getElementById('passenger-name').value,
        age: parseInt(document.getElementById('passenger-age').value),
        gender: document.getElementById('passenger-gender').value,
        adhaar_no: document.getElementById('passenger-adhaar').value,
        mobile_no: document.getElementById('passenger-mobile').value,
        seat_number: parseInt(document.getElementById('book-seat-number').value),
        payment_mode: document.getElementById('payment-mode').value
    };

    try {
        const response = await fetch(`${API_URL}/bookings/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}` // The VIP Pass!
            },
            body: JSON.stringify(bookingData)
        });

        if (response.ok) {
            alert("🎉 Ticket Booked Successfully!");
            window.location.href = "my_bookings.html"; // Redirect to their tickets!
        } else {
            const errorData = await response.json();
            alert(`Error: ${errorData.detail}`);
        }
    } catch (error) {
        console.error("Booking error:", error);
    }
});