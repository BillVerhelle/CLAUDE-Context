#!/usr/bin/env python3
"""Zillow Tracker - No Duplicates + Netlify Deployment"""

import requests
import json
import time
import os
from datetime import datetime

# API Configuration
API_KEY = "2fce36f1bamsh4969a56fe56ac45p180e3cjsn208af5507053"
headers = {
    'x-rapidapi-host': 'zillow-com1.p.rapidapi.com',
    'x-rapidapi-key': API_KEY
}

print("🏠 Zillow Property Tracker - Netlify Version")
print("=" * 60)

# Dictionary to store unique properties by zpid
unique_properties = {}

locations = [
    "Franklin, TN 37064",
    "Brentwood, TN 37027",
    "College Grove, TN 37046",
    "Cool Springs, TN 37067"
]

for location in locations:
    print(f"\n📍 Fetching {location}...")

    for page in range(1, 4):  # 3 pages per location
        print(f"   Page {page}...", end="")

        url = "https://zillow-com1.p.rapidapi.com/propertyExtendedSearch"
        params = {
            "location": location,
            "status_type": "ForSale",
            "home_type": "Houses",
            "minPrice": "2000000",
            "maxPrice": "8000000",
            "page": page
        }

        try:
            response = requests.get(url, headers=headers, params=params, timeout=15)

            if response.status_code == 200:
                data = response.json()

                if 'props' in data and data['props']:
                    props = data['props']
                    new_count = 0

                    for prop in props:
                        zpid = prop.get('zpid', '')

                        # Skip duplicates
                        if zpid and zpid not in unique_properties:
                            image_url = prop.get('imgSrc', '')
                            if not image_url and zpid:
                                image_url = f"https://photos.zillowstatic.com/fp/{zpid}-cc_ft_768.webp"

                            unique_properties[zpid] = {
                                'zpid': zpid,
                                'address': prop.get('address', ''),
                                'city': location.split(',')[0],
                                'price': int(prop.get('price', 0)),
                                'bedrooms': prop.get('bedrooms', 0),
                                'bathrooms': prop.get('bathrooms', 0),
                                'sqft': prop.get('livingArea', 0),
                                'image_url': image_url,
                                'url': f"https://www.zillow.com{prop.get('detailUrl', '')}",
                                'daysOnZillow': prop.get('daysOnZillow', 0),
                                'listingStatus': prop.get('listingStatus', '')
                            }
                            new_count += 1

                    print(f" {new_count} new properties (total: {len(unique_properties)})")

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

        time.sleep(0.5)

# Convert to list and sort by price
all_properties = list(unique_properties.values())
all_properties.sort(key=lambda x: x['price'], reverse=True)  # Highest price first

print(f"\n✅ Total unique properties: {len(all_properties)}")

# Create public folder for Netlify
os.makedirs('public', exist_ok=True)

# Generate single-page website
html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tennessee Luxury Properties - {len(all_properties)} Homes</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }}
        .header {{
            background: rgba(255, 255, 255, 0.98);
            padding: 30px;
            box-shadow: 0 2px 20px rgba(0,0,0,0.1);
            position: sticky;
            top: 0;
            z-index: 100;
        }}
        .container {{ max-width: 1400px; margin: 0 auto; padding: 20px; }}
        h1 {{
            font-size: 48px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
        }}
        .stats {{
            display: flex;
            gap: 30px;
            margin: 20px 0;
            flex-wrap: wrap;
        }}
        .stat {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 25px;
            border-radius: 25px;
            font-weight: 600;
        }}
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
            gap: 25px;
            margin: 30px 0;
        }}
        .property {{
            background: white;
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
            cursor: pointer;
        }}
        .property:hover {{
            transform: translateY(-10px);
            box-shadow: 0 20px 40px rgba(0,0,0,0.2);
        }}
        .img-container {{
            position: relative;
            height: 250px;
            background: linear-gradient(to bottom, transparent, rgba(0,0,0,0.3));
            overflow: hidden;
        }}
        .img-container img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform 0.3s;
        }}
        .property:hover img {{
            transform: scale(1.1);
        }}
        .new-badge {{
            position: absolute;
            top: 10px;
            right: 10px;
            background: #00c896;
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-weight: 600;
            font-size: 12px;
        }}
        .details {{
            padding: 20px;
        }}
        .price {{
            font-size: 32px;
            font-weight: bold;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 10px 0;
        }}
        .address {{
            font-weight: 600;
            font-size: 18px;
            color: #333;
            margin-bottom: 5px;
        }}
        .city {{
            color: #666;
            margin-bottom: 10px;
        }}
        .specs {{
            display: flex;
            gap: 15px;
            color: #888;
            font-size: 14px;
            margin: 15px 0;
        }}
        .view-btn {{
            display: inline-block;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 10px 20px;
            border-radius: 25px;
            text-decoration: none;
            font-weight: 600;
            transition: all 0.3s;
        }}
        .view-btn:hover {{
            transform: scale(1.05);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }}
        .footer {{
            text-align: center;
            padding: 50px 20px;
            color: white;
        }}
        @media (max-width: 768px) {{
            h1 {{ font-size: 32px; }}
            .grid {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <div class="container">
            <h1>🏠 Tennessee Luxury Properties</h1>
            <p style="font-size: 20px; color: #666;">Live data from {len(all_properties)} premium listings</p>
            <div class="stats">
                <div class="stat">Franklin: {len([p for p in all_properties if p['city'] == 'Franklin'])}</div>
                <div class="stat">Brentwood: {len([p for p in all_properties if p['city'] == 'Brentwood'])}</div>
                <div class="stat">College Grove: {len([p for p in all_properties if p['city'] == 'College Grove'])}</div>
                <div class="stat">$2M-$8M Range</div>
            </div>
        </div>
    </div>

    <div class="container">
        <div class="grid">
'''

# Add top 100 properties
for prop in all_properties[:100]:
    new_badge = '<span class="new-badge">NEW</span>' if prop['daysOnZillow'] <= 7 else ''

    html += f'''
            <div class="property" onclick="window.open('{prop['url']}', '_blank')">
                <div class="img-container">
                    <img src="{prop['image_url']}" alt="{prop['address']}" loading="lazy">
                    {new_badge}
                </div>
                <div class="details">
                    <div class="address">{prop['address']}</div>
                    <div class="city">{prop['city']}, TN</div>
                    <div class="price">${prop['price']:,}</div>
                    <div class="specs">
                        <span>🛏 {prop['bedrooms']} beds</span>
                        <span>🚿 {prop['bathrooms']} baths</span>
                        <span>📐 {prop['sqft']:,} sqft</span>
                    </div>
                    <a href="{prop['url']}" target="_blank" class="view-btn">View on Zillow</a>
                </div>
            </div>
'''

html += f'''
        </div>
    </div>

    <div class="footer">
        <p>Showing top 100 of {len(all_properties)} properties</p>
        <p style="margin-top: 10px; opacity: 0.8;">Last updated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
    </div>
</body>
</html>
'''

# Save to public folder
with open('public/index.html', 'w') as f:
    f.write(html)

# Create netlify.toml for deployment
with open('netlify.toml', 'w') as f:
    f.write('''[build]
  publish = "public"

[[headers]]
  for = "/*"
  [headers.values]
    X-Frame-Options = "DENY"
    X-Content-Type-Options = "nosniff"
''')

print("\n✅ Website generated in 'public' folder")
print("\n📦 To deploy to Netlify:")
print("1. Install Netlify CLI: npm install -g netlify-cli")
print("2. Deploy: netlify deploy --dir=public --prod")
print("3. Or drag the 'public' folder to netlify.com/drop")
print("\n🌐 Preview locally: open public/index.html")