#!/usr/bin/env python3
"""Complete Zillow Tracker with All Fixes"""

import requests
import json
import time
from datetime import datetime

# API Configuration
API_KEY = "2fce36f1bamsh4969a56fe56ac45p180e3cjsn208af5507053"
headers = {
    'x-rapidapi-host': 'zillow-com1.p.rapidapi.com',
    'x-rapidapi-key': API_KEY
}

print("🏠 Complete Zillow Property Tracker")
print("=" * 60)
print("Fixes applied:")
print("✅ 1. Fetching 300+ properties with pagination")
print("✅ 2. Showing 100 properties per page")
print("✅ 3. Sorting by price (low to high)")
print("✅ 4. Including property images")
print("✅ 5. Proper badges (New, Price Change, The Grove)")
print("=" * 60)

all_properties = []

# Fetch from all locations with pagination
locations = [
    "Franklin, TN 37064",
    "Brentwood, TN 37027",
    "College Grove, TN 37046",
    "Cool Springs, TN 37067"
]

for location in locations:
    print(f"\n📍 Fetching {location}...")

    for page in range(1, 6):  # Fetch 5 pages per location
        print(f"   Page {page}...", end="")

        url = "https://zillow-com1.p.rapidapi.com/propertyExtendedSearch"
        params = {
            "location": location,
            "status_type": "ForSale",
            "home_type": "Houses",
            "minPrice": "2500000",
            "maxPrice": "6000000",
            "minBeds": "4",
            "yearBuiltMin": "2015",
            "page": page
        }

        try:
            response = requests.get(url, headers=headers, params=params, timeout=15)

            if response.status_code == 200:
                data = response.json()

                if 'props' in data and data['props']:
                    props = data['props']

                    for prop in props:
                        # Extract image
                        image_url = prop.get('imgSrc', '')
                        if not image_url and 'zpid' in prop:
                            image_url = f"https://photos.zillowstatic.com/fp/{prop['zpid']}-cc_ft_384.webp"

                        # Determine badges
                        badges = []

                        # New listing check
                        if prop.get('daysOnZillow', 100) <= 30:
                            badges.append("New")

                        # Price change check
                        if prop.get('priceChange', 0) != 0:
                            badges.append("Price Change")

                        # Grove check
                        address = prop.get('address', '')
                        if 'Grove' in address:
                            badges.append("The Grove")

                        property_data = {
                            'address': address,
                            'city': location.split(',')[0],
                            'state': 'TN',
                            'price': int(prop.get('price', 0)),
                            'bedrooms': prop.get('bedrooms', 0),
                            'bathrooms': prop.get('bathrooms', 0),
                            'sqft': prop.get('livingArea', 0),
                            'yearBuilt': prop.get('yearBuilt', 0),
                            'image_url': image_url,
                            'url': f"https://www.zillow.com/homedetails/{prop.get('zpid', '')}_zpid/",
                            'badges': badges
                        }

                        all_properties.append(property_data)

                    print(f" {len(props)} properties")

                    if len(props) < 40:
                        break
                else:
                    print(" No more")
                    break
            else:
                print(f" Error {response.status_code}")
                break

        except Exception as e:
            print(f" Error: {e}")
            break

        time.sleep(0.5)  # Rate limiting

# Sort by price (low to high)
all_properties.sort(key=lambda x: x['price'])

print(f"\n✅ Total properties found: {len(all_properties)}")

# Save data
with open('all_properties.json', 'w') as f:
    json.dump(all_properties, f, indent=2)

print(f"💾 Saved to all_properties.json")

# Generate website with pagination
print("\n📄 Generating website...")

properties_per_page = 100
total_pages = (len(all_properties) + properties_per_page - 1) // properties_per_page

for page_num in range(1, total_pages + 1):
    start = (page_num - 1) * properties_per_page
    end = min(start + properties_per_page, len(all_properties))
    page_props = all_properties[start:end]

    html = f'''<!DOCTYPE html>
<html>
<head>
    <title>Cyndee TN Home Search - Page {page_num}/{total_pages}</title>
    <style>
        body {{ font-family: -apple-system, sans-serif; background: #f5f5f7; margin: 0; }}
        .header {{ background: white; padding: 30px; border-bottom: 1px solid #ddd; }}
        h1 {{ font-size: 48px; margin: 0; }}
        .container {{ max-width: 1400px; margin: 0 auto; padding: 20px; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 20px; margin: 20px 0; }}
        .property {{ background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
        .property:hover {{ transform: translateY(-2px); box-shadow: 0 4px 16px rgba(0,0,0,0.15); }}
        .img-container {{ position: relative; height: 200px; background: #ddd; }}
        .img-container img {{ width: 100%; height: 100%; object-fit: cover; }}
        .badges {{ position: absolute; top: 10px; left: 10px; }}
        .badge {{ background: #00c896; color: white; padding: 4px 8px; border-radius: 20px; font-size: 11px; display: inline-block; margin-right: 5px; }}
        .badge.price-change {{ background: #ff3b30; }}
        .badge.the-grove {{ background: #5856d6; }}
        .details {{ padding: 15px; }}
        .address {{ font-weight: 600; margin-bottom: 5px; }}
        .price {{ color: #0071e3; font-size: 24px; font-weight: 600; margin: 10px 0; }}
        .specs {{ color: #666; font-size: 14px; }}
        .pagination {{ text-align: center; margin: 40px 0; }}
        .page-btn {{ padding: 10px 20px; margin: 0 5px; background: white; border: 1px solid #ddd; text-decoration: none; color: #333; border-radius: 8px; }}
        .page-btn:hover {{ background: #0071e3; color: white; }}
        .page-btn.active {{ background: #000; color: white; }}
    </style>
</head>
<body>
    <div class="header">
        <div class="container">
            <h1>🏠 Cyndee TN Home Search</h1>
            <p>Page {page_num} of {total_pages} • {len(all_properties)} total properties • Sorted by price (low to high)</p>
        </div>
    </div>

    <div class="container">
        <div class="grid">
'''

    for prop in page_props:
        badges_html = ''.join([f'<span class="badge {b.lower().replace(" ", "-")}">{b}</span>' for b in prop['badges']])

        html += f'''
            <div class="property">
                <div class="img-container">
                    <img src="{prop['image_url']}" alt="{prop['address']}">
                    <div class="badges">{badges_html}</div>
                </div>
                <div class="details">
                    <div class="address">{prop['address']}</div>
                    <div>{prop['city']}, TN</div>
                    <div class="price">${prop['price']:,}</div>
                    <div class="specs">
                        {prop['bedrooms']} beds • {prop['bathrooms']} baths • {prop['sqft']:,} sqft
                    </div>
                    <a href="{prop['url']}" target="_blank" style="color: #0071e3; text-decoration: none;">View on Zillow →</a>
                </div>
            </div>
'''

    html += '''
        </div>

        <div class="pagination">
'''

    # Add pagination links
    for p in range(1, total_pages + 1):
        active = "active" if p == page_num else ""
        html += f'            <a href="page_{p}.html" class="page-btn {active}">{p}</a>\n'

    html += f'''
        </div>
    </div>

    <p style="text-align: center; color: #666;">
        Last updated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}
    </p>
</body>
</html>
'''

    filename = f'website/page_{page_num}.html'
    with open(filename, 'w') as f:
        f.write(html)

# Create index.html that redirects to page 1
with open('website/index.html', 'w') as f:
    f.write('''<!DOCTYPE html>
<html>
<head>
    <title>Cyndee TN Home Search</title>
    <meta http-equiv="refresh" content="0; url=page_1.html">
</head>
<body>
    <p>Redirecting to property listings...</p>
</body>
</html>''')

print(f"✅ Website generated with {total_pages} pages")
print(f"🌐 Open website/index.html to view")