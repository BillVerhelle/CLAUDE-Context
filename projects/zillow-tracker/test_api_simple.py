#!/usr/bin/env python3
"""
Simplified test script for Zillow property data retrieval
Tests basic HTTP requests without Selenium dependency
"""

import requests
import json
from bs4 import BeautifulSoup
import time
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class ZillowAPITester:
    """Test methods to retrieve Zillow property data"""

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Connection': 'keep-alive',
            'Referer': 'https://www.google.com/',
        }

    def test_direct_request(self, zpid: str):
        """Test direct HTTP request to Zillow"""
        print("\n=== Testing Direct HTTP Request ===")
        url = f"https://www.zillow.com/homedetails/{zpid}_zpid/"

        try:
            print(f"Requesting: {url}")
            response = requests.get(url, headers=self.headers, timeout=10)
            print(f"Status Code: {response.status_code}")

            if response.status_code == 200:
                print("✓ Page retrieved successfully")

                # Save HTML for inspection
                with open('zillow_response.html', 'w', encoding='utf-8') as f:
                    f.write(response.text)
                print("  HTML saved to zillow_response.html for inspection")

                soup = BeautifulSoup(response.content, 'html.parser')

                # Try various selectors for price
                price_selectors = [
                    {'name': 'span', 'attrs': {'data-test': 'property-price'}},
                    {'name': 'span', 'class': 'Text-c11n-8-84-0__sc-aiai24-0'},
                    {'name': 'h3', 'class': 'home-summary-row'},
                ]

                for selector in price_selectors:
                    element = soup.find(**selector)
                    if element:
                        print(f"  Found element with {selector}: {element.text[:50]}...")
                        break

                # Check page title
                title = soup.find('title')
                if title:
                    print(f"  Page title: {title.text[:80]}...")

                return True
            elif response.status_code == 403:
                print("✗ Access forbidden (403) - May need different headers or proxy")
                return False
            elif response.status_code == 404:
                print("✗ Property not found (404)")
                return False
            else:
                print(f"✗ Failed with status code: {response.status_code}")
                return False

        except Exception as e:
            print(f"✗ Error: {e}")
            return False

    def test_search_request(self, address: str):
        """Test Zillow search functionality"""
        print("\n=== Testing Search Request ===")

        # Encode the address for URL
        from urllib.parse import quote
        encoded_address = quote(address)

        search_url = f"https://www.zillow.com/homes/{encoded_address}_rb/"

        try:
            print(f"Searching for: {address}")
            print(f"URL: {search_url}")

            response = requests.get(search_url, headers=self.headers, timeout=10)
            print(f"Status Code: {response.status_code}")

            if response.status_code == 200:
                print("✓ Search page retrieved")

                # Save search results
                with open('zillow_search.html', 'w', encoding='utf-8') as f:
                    f.write(response.text)
                print("  Search results saved to zillow_search.html")

                return True
            else:
                print(f"✗ Search failed with status: {response.status_code}")
                return False

        except Exception as e:
            print(f"✗ Error: {e}")
            return False

    def test_api_endpoints(self):
        """Test known Zillow API endpoints"""
        print("\n=== Testing API Endpoints ===")

        endpoints = [
            {
                'name': 'GetSearchPageState',
                'url': 'https://www.zillow.com/search/GetSearchPageState.htm',
                'method': 'GET'
            },
            {
                'name': 'Property Details API',
                'url': 'https://www.zillow.com/graphql',
                'method': 'POST'
            }
        ]

        for endpoint in endpoints:
            print(f"\nTesting {endpoint['name']}...")
            try:
                if endpoint['method'] == 'GET':
                    response = requests.get(endpoint['url'], headers=self.headers, timeout=5)
                else:
                    response = requests.post(endpoint['url'], headers=self.headers, timeout=5)

                print(f"  Status: {response.status_code}")

                if response.status_code == 200:
                    print(f"  ✓ Endpoint accessible")
                else:
                    print(f"  ✗ Endpoint returned {response.status_code}")

            except Exception as e:
                print(f"  ✗ Error: {str(e)[:50]}")


def main():
    """Main test function"""
    print("=== Zillow API Test Suite (Simplified) ===")
    print("This script tests methods to retrieve property data from Zillow")
    print("\nNote: Zillow has anti-scraping measures in place.")
    print("For production use, consider:")
    print("- Using official real estate APIs")
    print("- Implementing proxy rotation")
    print("- Adding delays between requests")
    print("- Respecting robots.txt and terms of service\n")

    tester = ZillowAPITester()

    # Test with a sample ZPID
    print("Example ZPID format: 12345678")
    print("You can find a ZPID in any Zillow property URL")
    print("Example: https://www.zillow.com/homedetails/123-Main-St/12345678_zpid/")

    test_zpid = input("\nEnter a Zillow Property ID (ZPID) to test (or press Enter to skip): ")

    results = {}

    if test_zpid.strip():
        results['Direct Request'] = tester.test_direct_request(test_zpid)

    # Test search
    address = input("\nEnter a property address to test search (or press Enter to skip): ")
    if address.strip():
        results['Search Request'] = tester.test_search_request(address)

    # Test API endpoints
    test_apis = input("\nTest API endpoints? (y/n): ")
    if test_apis.lower() == 'y':
        tester.test_api_endpoints()

    # Summary
    if results:
        print("\n=== Test Results Summary ===")
        for test_name, result in results.items():
            status = "✓ PASSED" if result else "✗ FAILED"
            print(f"{test_name}: {status}")

        print("\n=== Recommendations ===")
        if any(results.values()):
            print("• Some requests work - may need to handle anti-bot measures")
        else:
            print("• Direct scraping may be blocked")

        print("• Consider using alternative data sources:")
        print("  - Realty Mole API")
        print("  - Rentberry API")
        print("  - MLS data feeds")
        print("• Always respect website terms of service")


if __name__ == "__main__":
    main()