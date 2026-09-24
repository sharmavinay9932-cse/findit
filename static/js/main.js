document.addEventListener('DOMContentLoaded', () => {
    updateNavAuth();
});

function updateNavAuth() {
    const navAuthContainer = document.getElementById('nav-auth-container');
    if (!navAuthContainer) return;
    
    // Check if user is logged in
    fetch('/api/auth/me')
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                navAuthContainer.innerHTML = `
                    <a href="/dashboard">Dashboard</a>
                    <a href="#" id="nav-logout">Logout</a>
                `;
                document.getElementById('nav-logout').addEventListener('click', (e) => {
                    e.preventDefault();
                    logout();
                });
            } else {
                navAuthContainer.innerHTML = `
                    <a href="/login" class="btn btn-outline">Login</a>
                    <a href="/register" class="btn btn-primary">Get Started</a>
                `;
            }
        })
        .catch(err => {
            navAuthContainer.innerHTML = `
                <a href="/login" class="btn btn-outline">Login</a>
                <a href="/register" class="btn btn-primary">Get Started</a>
            `;
        });
}

function logout() {
    fetch('/api/auth/logout', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(() => {
        window.location.href = '/login';
    });
}
