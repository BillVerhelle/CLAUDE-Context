#!/usr/bin/env python3
"""
Fetch property data from Zillow RapidAPI
"""

import requests
import json
from datetime import datetime

# RapidAPI credentials
RAPIDAPI_KEY = "2fce36f1bamsh4969a56fe56ac45p180e3cjsn208af5507053"
RAPIDAPI_HOST = "zillow-com1.p.rapidapi.com"

def search_properties(location="Nashville, TN", home_type="Houses", min_price=2500000, max_price=6000000):
    """Search for properties using RapidAPI"""

    url = "https://zillow-com1.p.rapidapi.com/propertyExtendedSearch"

    params = {
        "location": location,
        "home_type": home_type,
        "minPrice": min_price,
        "maxPrice": max_price,
        "sort": "Price_High_Low"
    }

    headers = {
        "x-rapidapi-host": RAPIDAPI_HOST,
        "x-rapidapi-key": RAPIDAPI_KEY
    }

    print(f"🔍 Searching for luxury homes in {location}...")
    print(f"   Price range: ${min_price:,} - ${max_price:,}")

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()

        data = response.json()
        properties = data.get('props', [])

        print(f"✓ Found {len(properties)} properties\n")

        # Save raw data
        with open('api_properties.json', 'w') as f:
            json.dump(data, f, indent=2)

        # Display results
        for i, prop in enumerate(properties[:10], 1):
            print(f"{i}. {prop.get('address', 'N/A')}")
            print(f"   Price: ${prop.get('price', 0):,}")
            print(f"   {prop.get('bedrooms', 0)} beds, {prop.get('bathrooms', 0)} baths")
            print(f"   {prop.get('livingArea', 0):,} sqft")
            print(f"   ZPID: {prop.get('zpid', 'N/A')}")
            print(f"   Status: {prop.get('listingStatus', 'N/A')}")
            print()

        return properties

    except requests.exceptions.RequestException as e:
        print(f"❌ Error: {e}")
        return []

def get_property_details(zpid):
    """Get detailed info for a specific property"""

    url = "https://zillow-com1.p.rapidapi.com/property"

    params = {"zpid": zpid}

    headers = {
        "x-rapidapi-host": RAPIDAPI_HOST,
        "x-rapidapi-key": RAPIDAPI_KEY
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except:
        return None

if __name__ == "__main__":
    print("=== Zillow Luxury Property Search ===\n")

    # Search for luxury properties in different areas
    locations = [
        ("Franklin, TN", 2500000, 6000000),
        ("Brentwood, TN", 3000000, 7000000),
        ("College Grove, TN", 2000000, 5000000)
    ]

    all_properties = []

    for location, min_price, max_price in locations:
        properties = search_properties(location, "Houses", min_price, max_price)
        all_properties.extend(properties)

    # Save combined results
    output = {
        "timestamp": datetime.now().isoformat(),
        "total_properties": len(all_properties),
        "properties": all_properties
    }

    with open('luxury_properties.json', 'w') as f:
        json.dump(output, f, indent=2)

    print(f"\n✅ Saved {len(all_properties)} properties to luxury_properties.json")