import json
from datetime import datetime

# Load the real properties
with open('luxury_properties.json', 'r') as f:
    data = json.load(f)
    properties = data['properties']

print(f"🏠 Updating website with {len(properties)} real properties...")

# Count properties by city
franklin_count = len([p for p in properties if 'Franklin' in p.get('address', '')])
brentwood_count = len([p for p in properties if 'Brentwood' in p.get('address', '')])
college_grove_count = len([p for p in properties if 'College Grove' in p.get('address', '')])

# Generate HTML for the properties
html_content = '''<!DOCTYPE html>
<html>
<head>
    <title>Cyndee TN Home Search - Live Data</title>
    <style>
        body {
            font-family: -apple-system, sans-serif;
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f7;
        }
        h1 { font-size: 48px; }
        .stats {
            background: white;
            padding: 20px;
            border-radius: 12px;
            margin: 20px 0;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
        }
        .stat-box {
            text-align: center;
        }
        .stat-number {
            font-size: 36px;
            color: #0071e3;
            font-weight: bold;
        }
        .property {
            background: white;
            padding: 25px;
            margin: 20px 0;
            border-radius: 18px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
            transition: all 0.3s;
        }
        .property:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 30px rgba(0,0,0,0.12);
        }
        .price {
            color: #0071e3;
            font-size: 36px;
            font-weight: 600;
            margin: 10px 0;
        }
        .badge {
            display: inline-block;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 12px;
            color: white;
            margin-right: 8px;
            font-weight: 600;
        }
        .new { background: #00c896; }
        .grove { background: #5856d6; }
        .luxury { background: #ff9500; }
    </style>
</head>
<body>
    <h1>🏠 Cyndee TN Home Search - Live Zillow Data</h1>
    <p style="font-size: 20px; color: #666;">Real-time luxury properties from Zillow API</p>

    <div class="stats">
        <div class="stat-box">
            <div class="stat-number">''' + str(len(properties)) + '''</div>
            <div>Total Properties</div>
        </div>
        <div class="stat-box">
            <div class="stat-number">''' + str(franklin_count) + '''</div>
            <div>Franklin</div>
        </div>
        <div class="stat-box">
            <div class="stat-number">''' + str(brentwood_count) + '''</div>
            <div>Brentwood</div>
        </div>
        <div class="stat-box">
            <div class="stat-number">''' + str(college_grove_count) + '''</div>
            <div>College Grove</div>
        </div>
    </div>
'''

# Add top 20 properties
for prop in properties[:20]:
    badges = ''
    if prop.get('price', 0) >= 5000000:
        badges += '<span class="badge luxury">Luxury Estate</span>'
    if 'Grove' in prop.get('address', ''):
        badges += '<span class="badge grove">The Grove</span>'
    if prop.get('daysOnZillow', 0) <= 7:
        badges += '<span class="badge new">New</span>'

    # Extract city from address
    address_parts = prop.get('address', '').split(', ')
    city = address_parts[1] if len(address_parts) > 1 else ''
    zipcode = address_parts[2].split()[1] if len(address_parts) > 2 else ''

    html_content += f'''
    <div class="property">
        {badges}
        <h2>{prop.get('address', 'Address not available')}</h2>
        <div class="price">${prop.get('price', 0):,}</div>
        <div style="color: #666; margin: 10px 0;">
            {prop.get('bedrooms', '?')} beds • {prop.get('bathrooms', '?')} baths • {prop.get('livingArea', 0):,} sqft
        </div>
        <div style="color: #999; font-size: 14px;">
            ZPID: {prop.get('zpid', 'N/A')} • Listed {prop.get('daysOnZillow', '?')} days ago
        </div>
        <a href="https://www.zillow.com{prop.get('detailUrl', '')}" target="_blank" style="color: #0071e3; text-decoration: none;">View on Zillow →</a>
    </div>
    '''

html_content += f'''
    <p style="text-align: center; margin: 40px; color: #666;">
        Showing 20 of {len(properties)} properties • Updated {datetime.now().strftime('%B %d, %Y at %I:%M %p')}
    </p>
</body>
</html>
'''

# Save the updated website
with open('website/index.html', 'w') as f:
    f.write(html_content)

print("✅ Website updated with real Zillow data!")
print(f"📊 Stats:")
print(f"   - Total: {len(properties)} properties")
print(f"   - Franklin: {franklin_count}")
print(f"   - Brentwood: {brentwood_count}")
print(f"   - College Grove: {college_grove_count}")
print("\n🌐 View at: http://localhost:8080 or open website/index.html")