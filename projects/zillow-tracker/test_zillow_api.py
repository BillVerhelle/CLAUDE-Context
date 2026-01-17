import requests
import json

print("🏠 Testing Zillow API for Tennessee Properties...")
print("=" * 50)

# Your API credentials
headers = {
    'x-rapidapi-host': 'zillow-com1.p.rapidapi.com',
    'x-rapidapi-key': '2fce36f1bamsh4969a56fe56ac45p180e3cjsn208af5507053'
}

# Test 1: Search properties in Franklin, TN
print("\n1. Searching Franklin, TN (37064)...")
url = "https://zillow-com1.p.rapidapi.com/propertyExtendedSearch"
params = {
    "location": "Franklin, TN 37064",
    "status_type": "ForSale",
    "minPrice": "2500000",
    "maxPrice": "6000000"
}

response = requests.get(url, headers=headers, params=params)
print(f"   Status: {response.status_code}")

if response.status_code == 200:
    print("   ✅ SUCCESS - API is working!")
    data = response.json()
    if 'props' in data:
        print(f"   Found {len(data['props'])} properties")
elif response.status_code == 403:
    print("   ❌ API Key needs subscription")
    print("\n   TO ACTIVATE:")
    print("   1. Go to: https://rapidapi.com/apimaker/api/zillow-com1")
    print("   2. Click 'Subscribe to Test'")
    print("   3. Choose Basic (FREE - 500 requests/month)")
    print("   4. Test again")
else:
    print(f"   Error: {response.text[:100]}")

print("\n" + "=" * 50)