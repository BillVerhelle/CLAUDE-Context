#!/usr/bin/env python3
"""Generate Complete Multi-Page Netlify Site"""

import json
import os
from datetime import datetime

print("🏠 Generating Complete Netlify Site...")
print("=" * 60)

# Load property data
try:
    with open('all_properties.json', 'r') as f:
        properties = json.load(f)
except:
    try:
        with open('luxury_properties.json', 'r') as f:
            properties = json.load(f)['properties']
    except:
        print("❌ No property data found!")
        exit(1)

# Ensure properties are sorted by price
properties.sort(key=lambda x: x.get('price', 0))

print(f"✅ Found {len(properties)} properties")

# Create public directory
os.makedirs('public', exist_ok=True)

# Settings
properties_per_page = 100
total_pages = (len(properties) + properties_per_page - 1) // properties_per_page

print(f"📄 Creating {total_pages} pages (100 properties each)...")

# Create CSS file
css_content = """
body {
    font-family: -apple-system, BlinkMacSystemFont, sans-serif;
    margin: 0;
    background: #f5f5f7;
}
.header {
    background: white;
    padding: 30px;
    border-bottom: 1px solid #ddd;
    position: sticky;
    top: 0;
    z-index: 100;
}
h1 {
    font-size: 48px;
    margin: 0;
    letter-spacing: -1px;
}
.subtitle {
    color: #666;
    margin-top: 10px;
}
.container {
    max-width: 1400px;
    margin: 0 auto;
    padding: 20px;
}
.stats {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 20px;
    margin: 30px 0;
}
.stat-box {
    background: white;
    padding: 15px;
    border-radius: 12px;
    text-align: center;
}
.stat-number {
    font-size: 28px;
    color: #0071e3;
    font-weight: 600;
}
.grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 20px;
    margin: 30px 0;
}
.property {
    background: white;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    transition: transform 0.2s;
}
.property:hover {
    transform: translateY(-4px);
    box-shadow: 0 4px 16px rgba(0,0,0,0.15);
}
.img-container {
    height: 200px;
    background: #ddd;
    position: relative;
}
.img-container img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}
.badges {
    position: absolute;
    top: 10px;
    left: 10px;
    display: flex;
    gap: 5px;
}
.badge {
    background: #00c896;
    color: white;
    padding: 4px 10px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 600;
}
.badge.price-change {
    background: #ff3b30;
}
.badge.the-grove {
    background: #5856d6;
}
.details {
    padding: 15px;
}
.address {
    font-weight: 600;
    font-size: 16px;
    margin-bottom: 5px;
}
.location {
    color: #666;
    font-size: 14px;
    margin-bottom: 10px;
}
.price {
    color: #0071e3;
    font-size: 24px;
    font-weight: 600;
    margin: 10px 0;
}
.specs {
    color: #666;
    font-size: 14px;
    padding-top: 10px;
    border-top: 1px solid #f0f0f0;
}
.pagination {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 10px;
    margin: 40px 0;
    flex-wrap: wrap;
}
.page-btn {
    padding: 10px 20px;
    background: white;
    border: 1px solid #ddd;
    border-radius: 8px;
    text-decoration: none;
    color: #333;
    transition: all 0.2s;
}
.page-btn:hover {
    background: #0071e3;
    color: white;
    border-color: #0071e3;
}
.page-btn.active {
    background: #000;
    color: white;
    border-color: #000;
}
.page-btn.disabled {
    opacity: 0.4;
    pointer-events: none;
}
footer {
    text-align: center;
    padding: 40px;
    color: #666;
    background: white;
    margin-top: 40px;
    border-top: 1px solid #ddd;
}
"""

with open('public/styles.css', 'w') as f:
    f.write(css_content)

# Generate each page
for page_num in range(1, total_pages + 1):
    start_idx = (page_num - 1) * properties_per_page
    end_idx = min(start_idx + properties_per_page, len(properties))
    page_properties = properties[start_idx:end_idx]

    print(f"   Creating page {page_num} (properties {start_idx + 1}-{end_idx})...")

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cyndee TN Home Search - Page {page_num} of {total_pages}</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div class="header">
        <div class="container">
            <h1>🏠 Cyndee TN Home Search</h1>
            <p class="subtitle">Luxury Tennessee Properties • $2.5M - $6M • Page {page_num} of {total_pages}</p>

            <div class="stats">
                <div class="stat-box">
                    <div class="stat-number">{len(properties)}</div>
                    <div>Total Properties</div>
                </div>
                <div class="stat-box">
                    <div class="stat-number">{start_idx + 1}-{end_idx}</div>
                    <div>Showing Now</div>
                </div>
                <div class="stat-box">
                    <div class="stat-number">{len([p for p in properties if p.get('daysOnZillow', 100) <= 30])}</div>
                    <div>New Listings</div>
                </div>
                <div class="stat-box">
                    <div class="stat-number">{len([p for p in properties if 'Grove' in p.get('address', '')])}</div>
                    <div>The Grove</div>
                </div>
            </div>
        </div>
    </div>

    <div class="container">
        <div class="grid">
"""

    # Add properties
    for prop in page_properties:
        # Generate badges HTML
        badges_html = ""
        if prop.get('daysOnZillow', 100) <= 30:
            badges_html += '<span class="badge">New</span>'
        if 'Grove' in prop.get('address', ''):
            badges_html += '<span class="badge the-grove">The Grove</span>'

        # Get image URL
        image_url = prop.get('image_url', prop.get('imgSrc', ''))
        if not image_url:
            zpid = prop.get('zpid', '')
            if zpid:
                image_url = f"https://photos.zillowstatic.com/fp/{zpid}-cc_ft_384.webp"
            else:
                image_url = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='400' height='300'%3E%3Crect fill='%23ddd' width='400' height='300'/%3E%3Ctext fill='%23999' x='50%25' y='50%25' text-anchor='middle' dy='.3em'%3ENo Image%3C/text%3E%3C/svg%3E"

        html += f"""
            <div class="property">
                <div class="img-container">
                    <img src="{image_url}" alt="{prop.get('address', '')}" loading="lazy">
                    <div class="badges">{badges_html}</div>
                </div>
                <div class="details">
                    <div class="address">{prop.get('address', 'Address Not Available')}</div>
                    <div class="location">{prop.get('city', '')}, TN</div>
                    <div class="price">${prop.get('price', 0):,}</div>
                    <div class="specs">
                        {prop.get('bedrooms', 0)} beds •
                        {prop.get('bathrooms', 0)} baths •
                        {prop.get('livingArea', prop.get('sqft', 0)):,} sqft
                    </div>
                    <a href="{prop.get('url', '#')}" target="_blank" style="color: #0071e3; font-size: 14px; display: block; margin-top: 10px;">
                        View on Zillow →
                    </a>
                </div>
            </div>
"""

    html += """
        </div>

        <div class="pagination">
"""

    # Add Previous button
    if page_num > 1:
        prev_file = "index.html" if page_num == 2 else f"page{page_num - 1}.html"
        html += f'<a href="{prev_file}" class="page-btn">← Previous</a>'
    else:
        html += '<span class="page-btn disabled">← Previous</span>'

    # Add page number buttons
    for p in range(1, total_pages + 1):
        page_file = "index.html" if p == 1 else f"page{p}.html"
        active_class = "active" if p == page_num else ""
        html += f'<a href="{page_file}" class="page-btn {active_class}">{p}</a>'

    # Add Next button
    if page_num < total_pages:
        html += f'<a href="page{page_num + 1}.html" class="page-btn">Next →</a>'
    else:
        html += '<span class="page-btn disabled">Next →</span>'

    html += f"""
        </div>
    </div>

    <footer>
        <p>Showing properties {start_idx + 1} to {end_idx} of {len(properties)} total</p>
        <p>Data updated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
    </footer>
</body>
</html>
"""

    # Save the page
    if page_num == 1:
        filename = "public/index.html"
    else:
        filename = f"public/page{page_num}.html"

    with open(filename, 'w') as f:
        f.write(html)

# Create netlify.toml
netlify_config = """[build]
  publish = "."

[[redirects]]
  from = "/page1"
  to = "/index.html"
  status = 301
"""

with open('public/netlify.toml', 'w') as f:
    f.write(netlify_config)

print("\n✅ Website generation complete!")
print(f"   • Total pages created: {total_pages}")
print(f"   • Properties per page: 100")
print(f"   • Total properties: {len(properties)}")
print("\n📁 Files created in 'public' folder:")
print("   • index.html (page 1)")
for p in range(2, total_pages + 1):
    print(f"   • page{p}.html")
print("   • styles.css")
print("   • netlify.toml")
print("\n🚀 Ready to deploy to Netlify!")