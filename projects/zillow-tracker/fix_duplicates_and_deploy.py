#!/usr/bin/env python3
"""Fix Duplicates and Generate Clean Netlify Site"""

import json
import os
from datetime import datetime

print("🏠 Fixing Duplicates & Generating Clean Site")
print("=" * 60)

# Load all properties
try:
    with open('all_properties.json', 'r') as f:
        all_props = json.load(f)
    print(f"✅ Loaded {len(all_props)} total properties (with duplicates)")
except:
    print("❌ Can't find all_properties.json")
    exit(1)

# Remove duplicates using zpid as unique identifier
seen_zpids = set()
seen_addresses = set()
unique_properties = []
duplicate_count = 0

for prop in all_props:
    zpid = prop.get('zpid', '')
    address = prop.get('address', '').strip().lower()

    # Skip if we've seen this zpid OR this exact address
    if zpid and zpid in seen_zpids:
        duplicate_count += 1
        continue

    if address and address in seen_addresses:
        duplicate_count += 1
        continue

    # Add to unique properties
    if zpid:
        seen_zpids.add(zpid)
    if address:
        seen_addresses.add(address)

    unique_properties.append(prop)

print(f"✅ Removed {duplicate_count} duplicates")
print(f"✅ {len(unique_properties)} unique properties remaining")

# Sort by price (low to high)
unique_properties.sort(key=lambda x: x.get('price', 0))

# Count Grove properties
grove_count = len([p for p in unique_properties if any(
    grove in p.get('address', '').lower()
    for grove in ['grove', 'the grove', 'grove country club']
)])
print(f"✅ The Grove properties: {grove_count} (no duplicates)")

# Save clean data
with open('clean_properties.json', 'w') as f:
    json.dump(unique_properties, f, indent=2)

# Create public directory
os.makedirs('public', exist_ok=True)

# Generate website with 100 properties per page
properties_per_page = 100
total_pages = (len(unique_properties) + properties_per_page - 1) // properties_per_page

print(f"\n📄 Creating {total_pages} pages (100 properties each)...")

# Create CSS
css = """body{font-family:-apple-system,BlinkMacSystemFont,sans-serif;margin:0;background:#f5f5f7}
.header{background:white;padding:30px;border-bottom:1px solid #ddd;position:sticky;top:0;z-index:100}
h1{font-size:48px;margin:0}
.subtitle{color:#666;margin-top:10px}
.container{max-width:1400px;margin:0 auto;padding:20px}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:20px;margin:30px 0}
.stat-box{background:white;padding:15px;border-radius:12px;text-align:center}
.stat-number{font-size:28px;color:#0071e3;font-weight:600}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:20px;margin:30px 0}
.property{background:white;border-radius:12px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,0.1);transition:transform 0.2s}
.property:hover{transform:translateY(-4px);box-shadow:0 4px 16px rgba(0,0,0,0.15)}
.img-container{height:200px;background:#ddd;position:relative}
.img-container img{width:100%;height:100%;object-fit:cover}
.badges{position:absolute;top:10px;left:10px;display:flex;gap:5px}
.badge{background:#00c896;color:white;padding:4px 10px;border-radius:20px;font-size:11px;font-weight:600}
.badge.price-change{background:#ff3b30}
.badge.the-grove{background:#5856d6}
.details{padding:15px}
.address{font-weight:600;font-size:16px;margin-bottom:5px}
.location{color:#666;font-size:14px;margin-bottom:10px}
.price{color:#0071e3;font-size:24px;font-weight:600;margin:10px 0}
.specs{color:#666;font-size:14px;padding-top:10px;border-top:1px solid #f0f0f0}
.pagination{display:flex;justify-content:center;align-items:center;gap:10px;margin:40px 0;flex-wrap:wrap}
.page-btn{padding:10px 20px;background:white;border:1px solid #ddd;border-radius:8px;text-decoration:none;color:#333;transition:all 0.2s}
.page-btn:hover{background:#0071e3;color:white;border-color:#0071e3}
.page-btn.active{background:#000;color:white;border-color:#000}
.page-btn.disabled{opacity:0.4;pointer-events:none}
footer{text-align:center;padding:40px;color:#666;background:white;margin-top:40px;border-top:1px solid #ddd}"""

with open('public/styles.css', 'w') as f:
    f.write(css)

# Generate each page
for page_num in range(1, total_pages + 1):
    start = (page_num - 1) * properties_per_page
    end = min(start + properties_per_page, len(unique_properties))
    page_props = unique_properties[start:end]

    print(f"   Creating page {page_num} (properties {start + 1}-{end})...")

    # Count stats for this data
    new_count = len([p for p in unique_properties if 'New' in p.get('badges', [])])
    grove_on_page = len([p for p in page_props if any(
        g in p.get('address', '').lower() for g in ['grove', 'the grove']
    )])

    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Cyndee TN Home Search - Page {page_num}/{total_pages}</title>
<link rel="stylesheet" href="styles.css">
</head>
<body>
<div class="header">
<div class="container">
<h1>🏠 Cyndee TN Home Search</h1>
<p class="subtitle">Luxury Tennessee Properties • $2.5M-$6M • NO DUPLICATES</p>
<div class="stats">
<div class="stat-box"><div class="stat-number">{len(unique_properties)}</div><div>Total Unique</div></div>
<div class="stat-box"><div class="stat-number">{start+1}-{end}</div><div>Showing Now</div></div>
<div class="stat-box"><div class="stat-number">{grove_count}</div><div>The Grove</div></div>
<div class="stat-box"><div class="stat-number">Page {page_num}/{total_pages}</div><div>Current Page</div></div>
</div>
</div>
</div>
<div class="container">
<div class="grid">"""

    for prop in page_props:
        # Get image
        img = prop.get('image_url', '')
        if not img and prop.get('zpid'):
            img = f"https://photos.zillowstatic.com/fp/{prop['zpid']}-cc_ft_384.webp"
        if not img:
            img = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='400' height='300'%3E%3Crect fill='%23ddd' width='400' height='300'/%3E%3C/svg%3E"

        # Badges
        badges_html = ""
        for badge in prop.get('badges', []):
            badge_class = badge.lower().replace(' ', '-')
            badges_html += f'<span class="badge {badge_class}">{badge}</span>'

        # Check if Grove property
        if not badges_html and any(g in prop.get('address', '').lower() for g in ['grove', 'the grove']):
            badges_html = '<span class="badge the-grove">The Grove</span>'

        html += f"""
<div class="property">
<div class="img-container">
<img src="{img}" alt="{prop.get('address', '')}" loading="lazy">
<div class="badges">{badges_html}</div>
</div>
<div class="details">
<div class="address">{prop.get('address', 'Address Not Available')}</div>
<div class="location">{prop.get('city', '')}, TN {prop.get('zipcode', '')}</div>
<div class="price">${prop.get('price', 0):,}</div>
<div class="specs">{prop.get('bedrooms', 0)} beds • {prop.get('bathrooms', 0)} baths • {prop.get('livingArea', prop.get('sqft', 0)):,} sqft • Built {prop.get('yearBuilt', 'N/A')}</div>
<a href="{prop.get('url', '#')}" target="_blank" style="color:#0071e3;font-size:14px;display:block;margin-top:10px">View on Zillow →</a>
</div>
</div>"""

    html += '</div><div class="pagination">'

    # Previous button
    if page_num > 1:
        prev = "index.html" if page_num == 2 else f"page{page_num-1}.html"
        html += f'<a href="{prev}" class="page-btn">← Previous</a>'
    else:
        html += '<span class="page-btn disabled">← Previous</span>'

    # Page numbers
    for p in range(1, total_pages + 1):
        page_file = "index.html" if p == 1 else f"page{p}.html"
        active = "active" if p == page_num else ""
        html += f'<a href="{page_file}" class="page-btn {active}">{p}</a>'

    # Next button
    if page_num < total_pages:
        html += f'<a href="page{page_num+1}.html" class="page-btn">Next →</a>'
    else:
        html += '<span class="page-btn disabled">Next →</span>'

    html += f"""</div></div>
<footer>
<p>Showing {start+1}-{end} of {len(unique_properties)} UNIQUE properties (duplicates removed)</p>
<p>Updated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
</footer>
</body>
</html>"""

    filename = "public/index.html" if page_num == 1 else f"public/page{page_num}.html"
    with open(filename, 'w') as f:
        f.write(html)

print("\n✅ COMPLETE! Site ready with NO DUPLICATES")
print(f"📊 Final Stats:")
print(f"   • Unique properties: {len(unique_properties)}")
print(f"   • Duplicates removed: {duplicate_count}")
print(f"   • The Grove properties: {grove_count} (each listed once)")
print(f"   • Pages created: {total_pages}")

# List all files
print("\n📁 Files in public folder:")
for file in os.listdir('public'):
    print(f"   • {file}")