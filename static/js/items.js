document.addEventListener('DOMContentLoaded', () => {
    const browseItemsList = document.getElementById('browse-items-list');
    const recentItemsList = document.getElementById('recent-found-items');
    const searchInput = document.getElementById('search-input');
    const filterType = document.getElementById('filter-type');
    const filterCategory = document.getElementById('filter-category');
    
    let allItems = [];
    
    if (browseItemsList || recentItemsList) {
        fetch('/api/items')
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    allItems = data.data.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
                    
                    if (browseItemsList) {
                        renderItems(allItems, browseItemsList);
                    }
                    if (recentItemsList) {
                        const recentFound = allItems.filter(i => i.type === 'found').slice(0, 4);
                        renderItems(recentFound, recentItemsList);
                    }
                }
            });
    }
    
    if (searchInput) searchInput.addEventListener('input', filterItems);
    if (filterType) filterType.addEventListener('change', filterItems);
    if (filterCategory) filterCategory.addEventListener('change', filterItems);
    
    function filterItems() {
        const query = searchInput.value.toLowerCase();
        const type = filterType.value;
        const cat = filterCategory.value;
        
        const filtered = allItems.filter(item => {
            const matchesQuery = item.name.toLowerCase().includes(query) || 
                               (item.description && item.description.toLowerCase().includes(query)) ||
                               item.location.toLowerCase().includes(query);
            const matchesType = type === 'all' || item.type === type;
            const matchesCat = cat === 'all' || item.category === cat;
            
            return matchesQuery && matchesType && matchesCat;
        });
        
        renderItems(filtered, browseItemsList);
    }
    
    function renderItems(items, container) {
        if (items.length === 0) {
            container.innerHTML = '<p>No items found.</p>';
            return;
        }
        
        container.innerHTML = items.map(item => `
            <div class="item-card">
                ${item.image ? `<img src="/uploads/${item.type}/${item.image}" class="item-image" alt="${item.name}">` : `<div class="item-image" style="display:flex;align-items:center;justify-content:center;background:#e2e8f0;color:#64748b;">No Image</div>`}
                <div class="item-content">
                    <span class="badge ${item.type === 'lost' ? 'badge-lost' : 'badge-found'}">${item.type.toUpperCase()}</span>
                    <h3 class="item-title">${item.name}</h3>
                    <div class="item-details">
                        <p>📍 ${item.location}</p>
                        <p>📅 ${item.date}</p>
                        <p>🏷️ ${item.category}</p>
                    </div>
                    <a href="/item/${item.id}" class="btn btn-outline btn-block mt-auto">View Details</a>
                </div>
            </div>
        `).join('');
    }
    
    // Item Details logic
    if (typeof ITEM_ID !== 'undefined') {
        const itemDetailsContent = document.getElementById('item-details-content');
        fetch(`/api/items/${ITEM_ID}`)
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    const item = data.data;
                    itemDetailsContent.innerHTML = `
                        <div style="display:flex; gap: 2rem; flex-wrap: wrap;">
                            <div style="flex: 1; min-width: 300px;">
                                ${item.image ? `<img src="/uploads/${item.type}/${item.image}" style="width:100%; border-radius:8px;" alt="${item.name}">` : `<div style="width:100%; height:300px; display:flex;align-items:center;justify-content:center;background:#e2e8f0;color:#64748b; border-radius:8px;">No Image</div>`}
                            </div>
                            <div style="flex: 2; min-width: 300px;">
                                <span class="badge ${item.type === 'lost' ? 'badge-lost' : 'badge-found'}">${item.type.toUpperCase()}</span>
                                <h1 style="margin-bottom:1rem;">${item.name}</h1>
                                <p><strong>Status:</strong> ${item.status}</p>
                                <p><strong>Category:</strong> ${item.category}</p>
                                <p><strong>Brand:</strong> ${item.brand || 'N/A'}</p>
                                <p><strong>Color:</strong> ${item.color || 'N/A'}</p>
                                <p><strong>Location:</strong> ${item.location}</p>
                                <p><strong>Date:</strong> ${item.date} ${item.time || ''}</p>
                                <h3 style="margin-top:1rem;">Description</h3>
                                <p>${item.description || 'No description provided.'}</p>
                                <h3 style="margin-top:1rem;">Unique Features</h3>
                                <p>${item.unique_features || 'N/A'}</p>
                                
                                <div style="margin-top: 2rem; display: flex; gap: 1rem;">
                                    ${item.type === 'found' ? `<button class="btn btn-primary" onclick="alert('Claim process would start here!')">Claim Item</button>` : `<a href="/matches" class="btn btn-secondary">Check Matches</a>`}
                                </div>
                            </div>
                        </div>
                    `;
                } else {
                    itemDetailsContent.innerHTML = `<p>Item not found.</p>`;
                }
            })
            .catch(err => {
                itemDetailsContent.innerHTML = `<p>Error loading item.</p>`;
            });
    }
});
