// Property Tracker Web Application

let properties = [];

// Load properties on page load
document.addEventListener('DOMContentLoaded', function() {
    loadProperties();
});

// Load properties from API
async function loadProperties() {
    try {
        const response = await fetch('/api/properties');
        properties = await response.json();
        displayProperties();
    } catch (error) {
        console.error('Error loading properties:', error);
    }
}

// Display properties in grid
function displayProperties() {
    const grid = document.getElementById('properties-grid');

    if (properties.length === 0) {
        grid.innerHTML = '<div class="loading">No properties tracked yet. Click "Add Property" to get started!</div>';
        return;
    }

    grid.innerHTML = properties.map(property => {
        const changeClass = property.price_change > 0 ? 'positive' :
                          property.price_change < 0 ? 'negative' : 'neutral';
        const changeSymbol = property.price_change > 0 ? '+' : '';

        return `
            <div class="property-card">
                <div class="property-header">
                    <div class="property-address">${property.address}</div>
                    <div class="property-zpid">ZPID: ${property.zpid}</div>
                </div>

                <div class="property-price">
                    $${property.current_price?.toLocaleString() || 'N/A'}
                </div>

                <div class="price-change ${changeClass}">
                    ${changeSymbol}$${Math.abs(property.price_change || 0).toLocaleString()}
                    (${changeSymbol}${property.percent_change?.toFixed(2) || 0}%)
                </div>

                <div class="property-details">
                    <span>🛏️ ${property.bedrooms} beds</span>
                    <span>🚿 ${property.bathrooms} baths</span>
                    <span>📐 ${property.sqft} sqft</span>
                </div>

                <div class="property-actions">
                    <button onclick="showUpdatePriceModal('${property.zpid}', '${property.address}')">
                        Update Price
                    </button>
                    <button onclick="showPriceHistory('${property.zpid}')">
                        View History
                    </button>
                </div>
            </div>
        `;
    }).join('');
}

// Show add property modal
function showAddPropertyModal() {
    document.getElementById('addPropertyModal').style.display = 'block';
}

// Close modal
function closeModal() {
    document.getElementById('addPropertyModal').style.display = 'none';
    document.getElementById('addPropertyForm').reset();
}

// Show update price modal
function showUpdatePriceModal(zpid, address) {
    document.getElementById('updatePriceModal').style.display = 'block';
    document.getElementById('update-zpid').value = zpid;
    document.getElementById('update-address').textContent = address;
}

// Close update modal
function closeUpdateModal() {
    document.getElementById('updatePriceModal').style.display = 'none';
    document.getElementById('updatePriceForm').reset();
}

// Add property form submission
document.getElementById('addPropertyForm')?.addEventListener('submit', async function(e) {
    e.preventDefault();

    const propertyData = {
        zpid: document.getElementById('zpid').value,
        address: document.getElementById('address').value,
        price: document.getElementById('price').value,
        bedrooms: document.getElementById('bedrooms').value,
        bathrooms: document.getElementById('bathrooms').value,
        sqft: document.getElementById('sqft').value
    };

    try {
        const response = await fetch('/api/add_property', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(propertyData)
        });

        const result = await response.json();

        if (result.status === 'success') {
            closeModal();
            loadProperties();
            alert('Property added successfully!');
        }
    } catch (error) {
        console.error('Error adding property:', error);
        alert('Error adding property. Please try again.');
    }
});

// Update price form submission
document.getElementById('updatePriceForm')?.addEventListener('submit', async function(e) {
    e.preventDefault();

    const updateData = {
        zpid: document.getElementById('update-zpid').value,
        price: document.getElementById('update-price').value
    };

    try {
        const response = await fetch('/api/update_price', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(updateData)
        });

        const result = await response.json();

        if (result.status === 'success') {
            closeUpdateModal();
            loadProperties();
            alert('Price updated successfully!');
        }
    } catch (error) {
        console.error('Error updating price:', error);
        alert('Error updating price. Please try again.');
    }
});

// Export data
async function exportData() {
    window.location.href = '/api/export';
}

// Show price history (placeholder for chart)
function showPriceHistory(zpid) {
    const property = properties.find(p => p.zpid === zpid);
    if (!property || !property.price_history) return;

    const history = property.price_history.map(h => {
        const date = new Date(h.date).toLocaleDateString();
        return `${date}: $${h.price.toLocaleString()}`;
    }).join('\n');

    alert(`Price History for ${property.address}:\n\n${history}`);
}

// Close modals when clicking outside
window.onclick = function(event) {
    if (event.target.className === 'modal') {
        event.target.style.display = 'none';
    }
}
