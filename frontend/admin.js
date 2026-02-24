const API_URL = "https://maharashtra-bus-booking-api.onrender.com";

// --- 1. STRICT ADMIN SECURITY CHECK ---
const token = localStorage.getItem('token');
const userRole = localStorage.getItem('user_role');
const userName = localStorage.getItem('user_name');

// If no token, OR if they are just a regular "user", kick them out!
if (!token || userRole !== 'admin') {
    alert("SECURITY ALERT: You do not have Admin privileges!");
    window.location.href = "login.html";
}

// Display Admin Name
document.addEventListener("DOMContentLoaded", () => {
    document.getElementById('admin-greeting').innerText = `Welcome Admin, ${userName}`;
    fetchAllBookings(); // Load all tickets automatically
});

function logout() {
    localStorage.clear();
    window.location.href = "login.html";
}

// --- 2. ADD A NEW BUS (WITH TOKEN) ---
document.getElementById('add-bus-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const busData = {
        bus_number: document.getElementById('bus-number').value,
        operator: document.getElementById('operator').value,
        source: document.getElementById('source').value,
        destination: document.getElementById('destination').value,
        date: document.getElementById('date').value,
        departure_time: document.getElementById('departure-time').value,
        total_seats: 40,
        price: parseFloat(document.getElementById('price').value)
    };

    try {
        const response = await fetch(`${API_URL}/buses/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}` // <--- ADMIN TOKEN!
            },
            body: JSON.stringify(busData)
        });

        if (response.ok) {
            alert('Bus added successfully!');
            document.getElementById('add-bus-form').reset();
        } else {
            const errorData = await response.json();
            alert(`Error adding bus: ${errorData.detail}`);
        }
    } catch (error) {
        console.error('Error:', error);
    }
});

// --- 3. FETCH ALL SYSTEM BOOKINGS (WITH TOKEN) ---
async function fetchAllBookings() {
    try {
        const response = await fetch(`${API_URL}/bookings/`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}` // <--- ADMIN TOKEN!
            }
        });

        if (response.status === 403) {
            alert("Forbidden: Your admin token is invalid.");
            logout();
            return;
        }

        const bookings = await response.json();
        const tbody = document.getElementById('bookings-body');
        tbody.innerHTML = ''; // Clear old data

        bookings.forEach(booking => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${booking.id}</td>
                <td>Bus #${booking.bus_id}</td>
                <td>${booking.passenger_name} <br><small>(${booking.mobile_no})</small></td>
                <td><b>${booking.seat_number}</b></td>
                <td>₹${booking.total_amount}</td>
            `;
            tbody.appendChild(tr);
        });
    } catch (error) {
        console.error('Error fetching bookings:', error);
    }
}

// --- 1. UI TAB SWITCHING LOGIC ---
function switchSection(sectionId, clickedTab) {
    // Hide all sections
    document.querySelectorAll('.admin-section').forEach(sec => sec.classList.remove('active-section'));
    // Show the targeted section
    document.getElementById(sectionId).classList.add('active-section');

    // Update the Sidebar styling to highlight the active tab
    document.querySelectorAll('.sidebar-menu li').forEach(li => li.classList.remove('active-tab'));
    clickedTab.classList.add('active-tab');

    // Auto-fetch data if a specific tab is opened
    if (sectionId === 'view-bookings') fetchAllBookings();
    if (sectionId === 'view-buses' || sectionId === 'view-routes') fetchAllBuses();
}

// --- HELPER FUNCTION: DRAW THE BUSES TABLE ---
function renderBusesTable(buses) {
    const tbody = document.getElementById('buses-body');
    tbody.innerHTML = '';

    buses.forEach(bus => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td><b>${bus.bus_number}</b></td>
            <td>${bus.operator}</td>
            <td>${bus.source} ➔ ${bus.destination}</td>
            <td>${bus.date} <br><small>${bus.departure_time}</small></td>
            <td>₹${bus.price}</td>
            <td style="display: flex; gap: 5px;">
                <button onclick="editBus(${bus.id})" style="padding: 6px 12px; font-size: 12px; width: auto; background-color: #f39c12; color: white; border: none; border-radius: 4px; cursor: pointer;">✏️ Edit</button>
                <button onclick="deleteBus(${bus.id})" class="danger" style="padding: 6px 12px; font-size: 12px; width: auto; border: none; border-radius: 4px; cursor: pointer;">🗑️ Delete</button>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

// --- 2. FETCH ALL BUSES & EXTRACT ROUTES ---
async function fetchAllBuses() {
    try {
        // Reset the title back to normal just in case it was filtered
        document.getElementById('manage-buses-title').innerText = "Active Fleet";

        const response = await fetch(`${API_URL}/buses/`);
        const buses = await response.json();

        // 1. Draw the full table
        renderBusesTable(buses);

        // 2. Extract Unique Routes
        let uniqueRoutesMap = new Map();
        buses.forEach(bus => {
            const routeKey = `${bus.source}-${bus.destination}`;
            if(!uniqueRoutesMap.has(routeKey)) {
                uniqueRoutesMap.set(routeKey, { source: bus.source, destination: bus.destination });
            }
        });

        // 3. Populate the "View Routes" list with Buttons!
        const routesList = document.getElementById('routes-list');
        routesList.innerHTML = '';
        uniqueRoutesMap.forEach(route => {
            const li = document.createElement('li');
            li.style.display = "flex";
            li.style.justifyContent = "space-between";
            li.style.alignItems = "center";
            li.style.padding = "10px";
            li.style.borderBottom = "1px solid #eee";
            li.innerHTML = `
                <strong style="font-size: 16px;">🛣️ ${route.source} ➔ ${route.destination}</strong>
                <button onclick="filterBusesByRoute('${route.source}', '${route.destination}')" style="width: auto; padding: 8px 15px; background: var(--secondary); color: white; border: none; border-radius: 5px; cursor: pointer;">🚌 View Buses on Route</button>
            `;
            routesList.appendChild(li);
        });

    } catch (error) {
        console.error('Error fetching buses:', error);
    }
}

// --- NEW FUNCTION: FILTER BUSES BY ROUTE ---
async function filterBusesByRoute(source, destination) {
    try {
        // 1. Switch the UI to the "Manage Buses" tab automatically
        const manageBusesTab = document.querySelectorAll('.sidebar-menu li')[2]; // The 3rd item in the sidebar
        switchSection('view-buses', manageBusesTab);

        // 2. Update the Title so the Admin knows it is filtered
        document.getElementById('manage-buses-title').innerHTML = `Filtered Fleet: <span style="color: var(--secondary);">${source} ➔ ${destination}</span>`;

        // 3. Fetch all buses, but only render the ones matching the route!
        const response = await fetch(`${API_URL}/buses/`);
        const allBuses = await response.json();

        const filteredBuses = allBuses.filter(bus => bus.source === source && bus.destination === destination);

        renderBusesTable(filteredBuses);

    } catch (error) {
        console.error('Error filtering route:', error);
    }
}

// --- NEW FUNCTION: EDIT BUS PLACEHOLDER ---
function editBus(busId) {
    alert(`Edit feature coming soon! (You clicked Edit for Bus ID: ${busId}) \n\nTo make this work fully, we would populate the "Add Bus" form with this bus's data and send a PUT request to the backend!`);
}

// --- 3. DELETE A BUS (SECURE ADMIN ACTION) ---
async function deleteBus(busId) {
    // 1. Ask for confirmation before deleting
    if (!confirm("Are you sure you want to delete this bus? This action cannot be undone.")) {
        return;
    }

    try {
        // 2. Send the delete request with the Admin Token
        const response = await fetch(`${API_URL}/buses/${busId}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (response.ok) {
            alert("Bus successfully removed from the fleet!");
            fetchAllBuses(); // Automatically refresh the table!
        } else {
            const errorData = await response.json();
            alert(`Error deleting bus: ${errorData.detail}`);
        }
    } catch (error) {
        console.error('Error deleting bus:', error);
        alert("Server error while trying to delete.");
    }
}