#!/bin/bash

# Zillow Property Tracker Website Builder
# This script creates a web interface for the property tracker

echo "========================================"
echo "Creating Web Interface for Property Tracker"
echo "========================================"
echo ""

# Create website directory structure
echo "Creating directory structure..."
mkdir -p website/{static/{css,js,images},templates}

# Create Flask application
echo "Creating Flask application..."
cat > website/app.py << 'PYTHON'
#!/usr/bin/env python3
"""
Flask web application for Zillow Property Tracker
"""

from flask import Flask, render_template, request, jsonify, send_file
import json
import os
import sys
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from zillow_property_tracker import ZillowPropertyTracker

app = Flask(__name__)
tracker = ZillowPropertyTracker(data_file='../property_data.json')


@app.route('/')
def index():
    """Home page with property dashboard"""
    return render_template('index.html')


@app.route('/api/properties')
def get_properties():
    """API endpoint to get all properties"""
    properties_list = []
    for zpid, data in tracker.properties.items():
        property_info = {
            'zpid': zpid,
            'address': data['address'],
            'bedrooms': data['bedrooms'],
            'bathrooms': data['bathrooms'],
            'sqft': data['sqft'],
            'date_added': data['date_added'],
            'price_history': data['price_history']
        }

        if data['price_history']:
            property_info['current_price'] = data['price_history'][-1]['price']
            property_info['initial_price'] = data['price_history'][0]['price']
            property_info['price_change'] = property_info['current_price'] - property_info['initial_price']
            property_info['percent_change'] = (property_info['price_change'] / property_info['initial_price'] * 100) if property_info['initial_price'] > 0 else 0

        properties_list.append(property_info)

    return jsonify(properties_list)


@app.route('/api/add_property', methods=['POST'])
def add_property():
    """API endpoint to add a new property"""
    data = request.json
    tracker.add_property(
        zpid=data['zpid'],
        address=data['address'],
        price=float(data['price']),
        bedrooms=int(data['bedrooms']),
        bathrooms=float(data['bathrooms']),
        sqft=int(data['sqft'])
    )
    return jsonify({'status': 'success', 'message': 'Property added successfully'})


@app.route('/api/update_price', methods=['POST'])
def update_price():
    """API endpoint to update property price"""
    data = request.json
    tracker.update_price(data['zpid'], float(data['price']))
    return jsonify({'status': 'success', 'message': 'Price updated successfully'})


@app.route('/api/export')
def export_csv():
    """Export data to CSV"""
    filename = 'property_export.csv'
    tracker.export_to_csv(filename)
    return send_file(filename, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
PYTHON

# Create HTML template
echo "Creating HTML template..."
cat > website/templates/index.html << 'HTML'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Zillow Property Tracker</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
    <div class="container">
        <header>
            <h1>🏠 Zillow Property Tracker</h1>
            <p>Monitor and track your properties</p>
        </header>

        <div class="actions">
            <button onclick="showAddPropertyModal()" class="btn btn-primary">+ Add Property</button>
            <button onclick="exportData()" class="btn btn-secondary">📊 Export to CSV</button>
            <button onclick="loadProperties()" class="btn btn-secondary">🔄 Refresh</button>
        </div>

        <div id="properties-grid" class="properties-grid">
            <!-- Properties will be loaded here -->
        </div>

        <!-- Add Property Modal -->
        <div id="addPropertyModal" class="modal">
            <div class="modal-content">
                <span class="close" onclick="closeModal()">&times;</span>
                <h2>Add New Property</h2>
                <form id="addPropertyForm">
                    <input type="text" id="zpid" placeholder="Zillow Property ID" required>
                    <input type="text" id="address" placeholder="Property Address" required>
                    <input type="number" id="price" placeholder="Current Price" step="1000" required>
                    <div class="form-row">
                        <input type="number" id="bedrooms" placeholder="Bedrooms" min="0" required>
                        <input type="number" id="bathrooms" placeholder="Bathrooms" min="0" step="0.5" required>
                        <input type="number" id="sqft" placeholder="Square Feet" min="0" required>
                    </div>
                    <button type="submit" class="btn btn-primary">Add Property</button>
                </form>
            </div>
        </div>

        <!-- Update Price Modal -->
        <div id="updatePriceModal" class="modal">
            <div class="modal-content">
                <span class="close" onclick="closeUpdateModal()">&times;</span>
                <h2>Update Property Price</h2>
                <form id="updatePriceForm">
                    <input type="hidden" id="update-zpid">
                    <p id="update-address"></p>
                    <input type="number" id="update-price" placeholder="New Price" step="1000" required>
                    <button type="submit" class="btn btn-primary">Update Price</button>
                </form>
            </div>
        </div>
    </div>

    <script src="{{ url_for('static', filename='js/app.js') }}"></script>
</body>
</html>
HTML

# Create CSS file
echo "Creating CSS styles..."
cat > website/static/css/style.css << 'CSS'
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
    padding: 20px;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
}

header {
    text-align: center;
    color: white;
    margin-bottom: 40px;
}

header h1 {
    font-size: 2.5em;
    margin-bottom: 10px;
}

header p {
    font-size: 1.2em;
    opacity: 0.9;
}

.actions {
    display: flex;
    gap: 15px;
    justify-content: center;
    margin-bottom: 30px;
}

.btn {
    padding: 12px 24px;
    border: none;
    border-radius: 8px;
    font-size: 16px;
    cursor: pointer;
    transition: all 0.3s;
    font-weight: 600;
}

.btn-primary {
    background: white;
    color: #667eea;
}

.btn-primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(0,0,0,0.2);
}

.btn-secondary {
    background: rgba(255,255,255,0.2);
    color: white;
    backdrop-filter: blur(10px);
}

.btn-secondary:hover {
    background: rgba(255,255,255,0.3);
}

.properties-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
    gap: 20px;
}

.property-card {
    background: white;
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    transition: transform 0.3s;
}

.property-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 25px rgba(0,0,0,0.15);
}

.property-header {
    border-bottom: 2px solid #f0f0f0;
    padding-bottom: 15px;
    margin-bottom: 15px;
}

.property-address {
    font-size: 1.2em;
    font-weight: 600;
    color: #333;
    margin-bottom: 5px;
}

.property-zpid {
    color: #666;
    font-size: 0.9em;
}

.property-price {
    font-size: 1.8em;
    font-weight: bold;
    color: #667eea;
    margin-bottom: 10px;
}

.price-change {
    display: inline-block;
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 0.9em;
    font-weight: 600;
}

.price-change.positive {
    background: #e6ffed;
    color: #00a854;
}

.price-change.negative {
    background: #ffebe6;
    color: #f5222d;
}

.price-change.neutral {
    background: #f0f0f0;
    color: #666;
}

.property-details {
    display: flex;
    gap: 15px;
    margin-top: 15px;
    font-size: 0.95em;
    color: #666;
}

.property-actions {
    display: flex;
    gap: 10px;
    margin-top: 15px;
}

.property-actions button {
    flex: 1;
    padding: 8px;
    border: 1px solid #ddd;
    border-radius: 6px;
    background: white;
    cursor: pointer;
    transition: all 0.2s;
}

.property-actions button:hover {
    background: #667eea;
    color: white;
    border-color: #667eea;
}

/* Modal Styles */
.modal {
    display: none;
    position: fixed;
    z-index: 1000;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0,0,0,0.5);
    animation: fadeIn 0.3s;
}

.modal-content {
    background-color: white;
    margin: 10% auto;
    padding: 30px;
    border-radius: 12px;
    width: 90%;
    max-width: 500px;
    animation: slideIn 0.3s;
}

.close {
    color: #aaa;
    float: right;
    font-size: 28px;
    font-weight: bold;
    cursor: pointer;
}

.close:hover {
    color: #000;
}

form {
    display: flex;
    flex-direction: column;
    gap: 15px;
}

form input {
    padding: 12px;
    border: 1px solid #ddd;
    border-radius: 6px;
    font-size: 16px;
}

form input:focus {
    outline: none;
    border-color: #667eea;
}

.form-row {
    display: flex;
    gap: 10px;
}

.form-row input {
    flex: 1;
}

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

@keyframes slideIn {
    from { transform: translateY(-50px); opacity: 0; }
    to { transform: translateY(0); opacity: 1; }
}

/* Loading spinner */
.loading {
    text-align: center;
    padding: 40px;
    color: white;
    font-size: 1.2em;
}

/* Chart container */
.chart-container {
    position: relative;
    height: 200px;
    margin-top: 15px;
}
CSS

# Create JavaScript file
echo "Creating JavaScript application..."
cat > website/static/js/app.js << 'JS'
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
JS

# Create requirements for web app
echo "Creating web requirements file..."
cat > website/requirements.txt << 'REQ'
Flask==3.0.0
Werkzeug==3.0.0
REQ

# Create run script
echo "Creating run script..."
cat > website/run.sh << 'BASH'
#!/bin/bash

echo "Starting Zillow Property Tracker Web Interface..."
echo "========================================"
echo ""

# Check if Flask is installed
if ! python3 -c "import flask" 2>/dev/null; then
    echo "Installing Flask..."
    pip3 install Flask
fi

# Start the Flask application
echo "Starting server on http://localhost:5000"
echo "Press Ctrl+C to stop the server"
echo ""

cd "$(dirname "$0")"
python3 app.py
BASH

chmod +x website/run.sh

echo ""
echo "========================================"
echo "Website created successfully!"
echo "========================================"
echo ""
echo "Directory structure:"
tree website/ 2>/dev/null || ls -R website/
echo ""
echo "To start the web interface:"
echo "  cd website"
echo "  ./run.sh"
echo ""
echo "Or manually:"
echo "  cd website"
echo "  python3 app.py"
echo ""
echo "Then open http://localhost:5000 in your browser"