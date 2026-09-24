document.addEventListener('DOMContentLoaded', () => {
    // Load dashboard stats
    const statLost = document.getElementById('stat-lost');
    const statFound = document.getElementById('stat-found');
    const userItemsList = document.getElementById('user-items-list');
    const welcomeMessage = document.getElementById('welcome-message');
    
    if (welcomeMessage) {
        fetch('/api/auth/me')
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    welcomeMessage.textContent = `Welcome, ${data.data.name}!`;
                    const profileDetails = document.getElementById('profile-details');
                    if (profileDetails) {
                        profileDetails.innerHTML = `
                            <p><strong>Name:</strong> ${data.data.name}</p>
                            <p><strong>Email:</strong> ${data.data.email}</p>
                            <p><strong>Member Since:</strong> ${data.data.member_since}</p>
                        `;
                    }
                } else {
                    window.location.href = '/login';
                }
            });
    }
    
    if (statLost || userItemsList) {
        fetch('/api/users/items')
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    const lost = data.data.lost;
                    const found = data.data.found;
                    
                    if (statLost) statLost.textContent = lost.length;
                    if (statFound) statFound.textContent = found.length;
                    
                    if (userItemsList) {
                        const allItems = [...lost, ...found].sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
                        if (allItems.length === 0) {
                            userItemsList.innerHTML = '<p>You haven\'t reported any items yet.</p>';
                        } else {
                            userItemsList.innerHTML = allItems.slice(0, 5).map(item => `
                                <div class="item-card">
                                    <div class="item-content">
                                        <span class="badge ${item.type === 'lost' ? 'badge-lost' : 'badge-found'}">${item.type.toUpperCase()}</span>
                                        <h3 class="item-title">${item.name}</h3>
                                        <div class="item-details">
                                            <p>📍 ${item.location}</p>
                                            <p>📅 ${item.date}</p>
                                            <p>🏷️ ${item.status}</p>
                                        </div>
                                        <a href="/item/${item.id}" class="btn btn-outline btn-block">View Details</a>
                                    </div>
                                </div>
                            `).join('');
                        }
                    }
                }
            });
    }
    
    const logoutBtn = document.getElementById('logout-btn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', (e) => {
            e.preventDefault();
            logout();
        });
    }
});
