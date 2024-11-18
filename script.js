// Example script for form handling
document.getElementById('loginForm')?.addEventListener('submit', (e) => {
    e.preventDefault();
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    // Make a login API call (example)
    fetch('/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.message === 'Login successful!') {
            window.location.href = 'dashboard.html'; // Redirect to dashboard
        } else {
            alert(data.error || 'Login failed!');
        }
    });
});
