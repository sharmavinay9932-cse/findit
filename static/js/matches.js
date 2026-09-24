document.addEventListener('DOMContentLoaded', () => {
    const lostItemSelect = document.getElementById('lost-item-select');
    const matchesList = document.getElementById('matches-list');
    
    if (lostItemSelect) {
        // Load user's lost items
        fetch('/api/users/items')
            .then(res => {
                if (res.status === 401) {
                    window.location.href = '/login';
                    return null;
                }
                return res.json();
            })
            .then(data => {
                if (data && data.success) {
                    const lostItems = data.data.lost;
                    if (lostItems.length === 0) {
                        lostItemSelect.innerHTML = '<option value="">You have no lost items reported.</option>';
                        lostItemSelect.disabled = true;
                    } else {
                        lostItems.forEach(item => {
                            const option = document.createElement('option');
                            option.value = item.id;
                            option.textContent = `${item.name} (${item.date})`;
                            lostItemSelect.appendChild(option);
                        });
                    }
                }
            });
            
        lostItemSelect.addEventListener('change', (e) => {
            const lostItemId = e.target.value;
            if (!lostItemId) {
                matchesList.innerHTML = '';
                return;
            }
            
            matchesList.innerHTML = '<p>Searching for potential matches...</p>';
            
            fetch(`/api/matches/${lostItemId}`)
                .then(res => res.json())
                .then(data => {
                    if (data.success) {
                        const matches = data.data;
                        if (matches.length === 0) {
                            matchesList.innerHTML = '<p>No potential matches found at this time.</p>';
                        } else {
                            matchesList.innerHTML = matches.map(match => {
                                const item = match.found_item;
                                return `
                                    <div class="item-card">
                                        ${item.image ? `<img src="/uploads/found/${item.image}" class="item-image" alt="${item.name}">` : `<div class="item-image" style="display:flex;align-items:center;justify-content:center;background:#e2e8f0;color:#64748b;">No Image</div>`}
                                        <div class="item-content">
                                            <div style="display: flex; justify-content: space-between; align-items: start;">
                                                <span class="badge badge-found">FOUND</span>
                                                <span class="badge" style="background-color: var(--primary-light); color: white;">Match: ${match.score}%</span>
                                            </div>
                                            <h3 class="item-title">${item.name}</h3>
                                            <p style="font-size: 0.875rem; color: var(--primary); font-weight: bold; margin-bottom: 0.5rem;">${match.classification}</p>
                                            <div class="item-details">
                                                <p>📍 ${item.location}</p>
                                                <p>📅 ${item.date}</p>
                                            </div>
                                            <a href="/item/${item.id}" class="btn btn-primary btn-block mt-auto">View Details & Claim</a>
                                        </div>
                                    </div>
                                `;
                            }).join('');
                        }
                    } else {
                        matchesList.innerHTML = `<p>Error loading matches: ${data.message}</p>`;
                    }
                })
                .catch(err => {
                    matchesList.innerHTML = '<p>Error loading matches.</p>';
                });
        });
    }
});
