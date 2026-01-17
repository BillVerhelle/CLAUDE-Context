#!/usr/bin/env python3
"""
Non-interactive test for Zillow property data retrieval
"""

import requests
from bs4 import BeautifulSoup
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class ZillowTester:
    """Test Zillow data retrieval methods"""

    def __init__(self):
        self.headers = {
            'User-Agent': os.getenv('USER_AGENT', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'),
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Connection': 'keep-alive',
        }

    def test_with_sample_zpid(self):
        """Test with a sample ZPID"""
        print("\n=== Testing with Sample ZPID ===")

        # Using a sample ZPID (this may or may not be valid)
        sample_zpid = "2060593428"  # Example ZPID
        url = f"https://www.zillow.com/homedetails/{sample_zpid}_zpid/"

        print(f"Testing URL: {url}")

        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            print(f"Status Code: {response.status_code}")

            if response.status_code == 200:
                print("✓ Page retrieved successfully")
                soup = BeautifulSoup(response.content, 'html.parser')

                # Check page title
                title = soup.find('title')
                if title:
                    print(f"Page title: {title.text[:100]}...")

                return True
            elif response.status_code == 403:
                print("✗ Access blocked (403) - Anti-bot protection active")
                return False
            elif response.status_code == 404:
                print("✗ Property not found (404)")
                return False
            else:
                print(f"✗ Unexpected status: {response.status_code}")
                return False

        except Exception as e:
            print(f"✗ Error: {e}")
            return False

    def test_search(self):
        """Test search functionality"""
        print("\n=== Testing Search ===")

        test_address = "Nashville, TN"
        search_url = f"https://www.zillow.com/homes/{test_address.replace(' ', '-')}_rb/"

        print(f"Searching for: {test_address}")
        print(f"URL: {search_url}")

        try:
            response = requests.get(search_url, headers=self.headers, timeout=10)
            print(f"Status Code: {response.status_code}")

            if response.status_code == 200:
                print("✓ Search page retrieved")
                return True
            elif response.status_code == 403:
                print("✗ Access blocked (403)")
                return False
            else:
                print(f"✗ Status: {response.status_code}")
                return False

        except Exception as e:
            print(f"✗ Error: {e}")
            return False

    def test_api_endpoint(self):
        """Test API endpoint"""
        print("\n=== Testing API Endpoint ===")

        api_url = "https://www.zillow.com/search/GetSearchPageState.htm"

        params = {
            'searchQueryState': json.dumps({
                'pagination': {},
                'usersSearchTerm': 'Nashville TN',
                'mapBounds': {},
                'filterState': {},
            })
        }

        print(f"Testing: {api_url}")

        try:
            response = requests.get(api_url, params=params, headers=self.headers, timeout=10)
            print(f"Status Code: {response.status_code}")

            if response.status_code == 200:
                print("✓ API endpoint accessible")
                return True
            else:
                print(f"✗ API returned: {response.status_code}")
                return False

        except Exception as e:
            print(f"✗ Error: {e}")
            return False


def main():
    print("=== Zillow Data Retrieval Test ===")
    print("Running automated tests...\n")

    tester = ZillowTester()

    # Run tests
    results = {
        'Sample ZPID Test': tester.test_with_sample_zpid(),
        'Search Test': tester.test_search(),
        'API Endpoint Test': tester.test_api_endpoint()
    }

    # Summary
    print("\n=== Test Results Summary ===")
    for test_name, passed in results.items():
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{test_name}: {status}")

    print("\n=== Analysis ===")
    if not any(results.values()):
        print("• All tests failed - Zillow has strong anti-bot protection")
        print("• This is expected behavior for direct scraping attempts")
    else:
        print("• Some tests passed - limited access possible")

    print("\n=== Recommendations ===")
    print("• Use the manual property tracker (zillow_property_tracker.py)")
    print("• For automated data: Consider official real estate APIs")
    print("• Alternative sources: Realty Mole, Rentberry, Realtor.com APIs")
    print("• Browser automation: Selenium with proper setup may work")
    print("• Always respect website terms of service")


if __name__ == "__main__":
    main()