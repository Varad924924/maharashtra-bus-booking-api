# 🚌 Maharashtra State Bus Booking System

A full-stack web application that allows users to search for buses, visually select seats, and book tickets. It also includes a secure Admin Dashboard to manage bus schedules and view all passenger bookings.

## 🛠️ Technology Stack
* **Backend:** Python, FastAPI
* **Database:** SQLite (managed via SQLAlchemy ORM)
* **Frontend:** HTML5, CSS3, Vanilla JavaScript
* **Authentication:** OAuth2 Password Bearer (Form Data)

## ✨ Key Features
**For Users:**
* **Bus Search:** Search for available buses by Source, Destination, and Travel Date.
* **Visual Seat Selection:** Interactive 40-seat grid. Real-time status showing Available (Green), Selected (Blue), and Booked (Red/Disabled) seats.
* **Booking System:** Captures detailed passenger information (Name, Age, Gender, Seat, Mobile, Adhaar, and Payment Mode).

**For Administrators:**
* **Secure Login:** Protected admin portal.
* **Dashboard:** View all system-wide bookings and revenue.
* **Bus Management (CRUD):** Add new buses, update pricing/timings, and delete canceled routes directly from the web interface.

## 🚀 How to Run the Project

This project requires two terminals to run simultaneously (one for the Backend API and one for the Frontend UI).

### Step 1: Start the Backend (FastAPI)
1. Open a terminal and navigate to the project folder.
2. Activate your virtual environment (if you are using one).
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   
### Start the Uvicorn server:
```bash
uvicorn app.main:app --reload
```

### The backend API will now be running at http://127.0.0.1:8000

### Step 2: Start the Frontend (Website)
Open a second terminal and navigate to the frontend folder:

```bash
cd frontend
````
Start the Python HTTP server:


```bash
python -m http.server 5500
```
The website will now be running at http://127.0.0.1:5500/index.html

🔐 Admin Credentials
To access the Admin Dashboard, navigate to login.html and use the following default credentials:

Username: varadgorhe0924@gmail.com

Password: Varad@924
(Note: Update these in the database for production environments).


# 🚌 Maharashtra Travels - Bus Booking API & Dashboard

A full-stack, production-ready Bus Booking System built with a secure RESTful API and a responsive, modern glassmorphism frontend. It features complete Role-Based Access Control (RBAC) separating regular passengers from system administrators.

---

## ✨ Key Features
* **Secure Authentication:** JWT (JSON Web Token) based login and registration.
* **Role-Based Access Control (RBAC):** Strict separation of User and Admin privileges.
* **Interactive UI:** Premium, responsive, mobile-friendly frontend using modern CSS and Vanilla JS.
* **Real-time Seat Mapping:** Dynamic visual seat selection preventing double-bookings.
* **Admin Dashboard:** God-mode control panel to manage the fleet, add routes, and view global sales.
* **Automated Data Seeding:** Includes a Python script to instantly generate 24 hours of scheduled buses for testing.

---

## 🛠️ Tech Stack
* **Backend:** Python, FastAPI, SQLAlchemy
* **Database:** SQLite (Relational Database)
* **Frontend:** HTML5, CSS3 (Glassmorphism & Flexbox/Grid), Vanilla JavaScript
* **Security:** Passlib (Bcrypt hashing), Python-Jose (JWT generation)

---

## 📡 API Architecture & Documentation

The system is powered by a decoupled backend API. Below is the data flow based on user roles.

### 👤 User Flow (Public & Private User Routes)
Users can browse available routes publicly, but must be authenticated to reserve a seat and view their ticket history.

| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `POST` | `/auth/signup` | Registers a new passenger account. | ❌ No |
| `POST` | `/auth/login` | Authenticates user and returns JWT token. | ❌ No |
| `POST` | `/buses/search` | Searches the public database for routes by date/city. | ❌ No |
| `POST` | `/bookings/` | Creates a new ticket reservation for a specific seat. | ✅ Yes (User) |
| `GET` | `/bookings/my-bookings` | Fetches only the digital tickets belonging to the logged-in user. | ✅ Yes (User) |

### 🛡️ Admin Flow (Protected Routes)
Admins have elevated privileges to modify the database. The API strictly validates the JWT role payload before executing these endpoints.

| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `POST` | `/buses/` | Publishes a new bus/route to the database. | ✅ Yes (Admin) |
| `GET` | `/buses/` | Retrieves the entire active fleet for management. | ✅ Yes (Admin) |
| `DELETE`| `/buses/{bus_id}` | Removes a bus and its associated data from the system. | ✅ Yes (Admin) |
| `GET` | `/bookings/` | Retrieves all tickets sold globally across the platform. | ✅ Yes (Admin) |

---

## 🚀 Local Setup & Installation

Follow these steps to run the application on your local machine or Wi-Fi network.

### 1. Start the Backend API
Open your terminal, activate your virtual environment, and run the FastAPI server:
```bash
# Start the server on your local network
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload