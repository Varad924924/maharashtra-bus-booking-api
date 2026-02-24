const API_URL = "http://192.168.1.37:8000";

// --- Toggle Between Login and Signup Forms ---
function toggleAuth(type) {
    if (type === 'login') {
        document.getElementById('login-form').style.display = 'block';
        document.getElementById('signup-form').style.display = 'none';
        document.getElementById('show-login').classList.add('active');
        document.getElementById('show-signup').classList.remove('active');
    } else {
        document.getElementById('login-form').style.display = 'none';
        document.getElementById('signup-form').style.display = 'block';
        document.getElementById('show-signup').classList.add('active');
        document.getElementById('show-login').classList.remove('active');
    }
}

// --- Handle User Sign Up ---
document.getElementById('signup-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const name = document.getElementById('signup-name').value;
    const email = document.getElementById('signup-email').value;
    const password = document.getElementById('signup-password').value;
    const messageEl = document.getElementById('signup-message');

    try {
        const response = await fetch(`${API_URL}/auth/signup`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, email, password })
        });

        const data = await response.json();

        if (response.ok) {
            messageEl.style.color = "green";
            messageEl.innerText = "Account created successfully! Please log in.";
            setTimeout(() => toggleAuth('login'), 2000); // Switch to login after 2 seconds
        } else {
            messageEl.style.color = "red";
            messageEl.innerText = data.detail[0]?.msg || data.detail || "Error creating account.";
        }
    } catch (error) {
        console.error("Signup error:", error);
    }
});

// --- Handle User & Admin Login ---
document.getElementById('login-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;
    const errorEl = document.getElementById('login-error');

    // FastAPI strictly expects x-www-form-urlencoded format for login
    const formData = new URLSearchParams();
    formData.append('username', email);
    formData.append('password', password);

    try {
        const response = await fetch(`${API_URL}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: formData
        });

        const data = await response.json();

        if (response.ok) {
            // SAVE THE DIGITAL KEY IN THE BROWSER!
            localStorage.setItem('token', data.access_token);
            localStorage.setItem('user_name', data.name);
            localStorage.setItem('user_role', data.role);

            // Redirect based on role
            if (data.role === 'admin') {
                window.location.href = "admin.html";
            } else {
                window.location.href = "index.html"; // Regular users go to the booking page
            }
        } else {
            errorEl.innerText = "Invalid email or password!";
        }
    } catch (error) {
        console.error("Login error:", error);
        errorEl.innerText = "Server error. Is the backend running?";
    }
});