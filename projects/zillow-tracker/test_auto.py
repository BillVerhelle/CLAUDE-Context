#!/usr/bin/env python3
"""
Automated test for Zillow data retrieval
"""

import requests
from bs4 import BeautifulSoup
import json

def test_zillow_access():
    """Test basic access to Zillow"""

    print("=== Automated Zillow Access Test ===\n")

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    }

    # Test 1: Homepage access
    print("Test 1: Accessing Zillow homepage...")
    try:
        response = requests.get('https://www.zillow.com', headers=headers, timeout=10)
        if response.status_code == 200:
            print(f"✓ Homepage accessible (Status: {response.status_code})")
            print(f"  Response size: {len(response.text)} bytes")
        else:
            print(f"✗ Homepage returned status: {response.status_code}")
    except Exception as e:
        print(f"✗ Error accessing homepage: {e}")

    # Test 2: Search page
    print("\nTest 2: Accessing search page...")
    try:
        search_url = "https://www.zillow.com/homes/Nashville,-TN_rb/"
        response = requests.get(search_url, headers=headers, timeout=10)
        if response.status_code == 200:
            print(f"✓ Search page accessible (Status: {response.status_code})")

            # Parse and look for property listings
            soup = BeautifulSoup(response.text, 'html.parser')
            scripts = soup.find_all('script', type='application/json')
            print(f"  Found {len(scripts)} JSON scripts in page")

            # Save for analysis
            with open('search_response.html', 'w') as f:
                f.write(response.text)
            print("  Saved to search_response.html for analysis")
        else:
            print(f"✗ Search page returned status: {response.status_code}")
    except Exception as e:
        print(f"✗ Error accessing search: {e}")

    # Test 3: Check robots.txt
    print("\nTest 3: Checking robots.txt...")
    try:
        response = requests.get('https://www.zillow.com/robots.txt', timeout=5)
        if response.status_code == 200:
            print("✓ Robots.txt accessible")
            lines = response.text.split('\n')[:10]
            print("  First few lines:")
            for line in lines[:5]:
                if line.strip():
                    print(f"    {line}")
        else:
            print(f"✗ Robots.txt returned status: {response.status_code}")
    except Exception as e:
        print(f"✗ Error accessing robots.txt: {e}")

    print("\n=== Summary ===")
    print("• Zillow is accessible but has anti-bot protection")
    print("• For production use, consider official APIs or data providers")
    print("• Always respect terms of service and robots.txt")
    print("\nAlternative data sources to consider:")
    print("• Realty Mole API (https://realtymole.com)")
    print("• Rentberry API (https://rentberry.com)")
    print("• Local MLS data feeds")
    print("• Realtor.com API")

if __name__ == "__main__":
    test_zillow_access()