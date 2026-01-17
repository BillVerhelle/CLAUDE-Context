#!/usr/bin/env python3
"""
Test script for Zillow property data retrieval
Tests various methods for accessing property information
"""

import requests
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class ZillowAPITester:
    """Test various methods to retrieve Zillow property data"""

    def __init__(self):
        self.headers = {
            'User-Agent': os.getenv('USER_AGENT', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'),
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Connection': 'keep-alive',
        }

    def test_direct_request(self, zpid: str):
        """Test direct HTTP request to Zillow"""
        print("\n=== Testing Direct HTTP Request ===")
        url = f"https://www.zillow.com/homedetails/{zpid}_zpid/"

        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            print(f"Status Code: {response.status_code}")

            if response.status_code == 200:
                print("Success! Page retrieved")
                soup = BeautifulSoup(response.content, 'html.parser')

                # Try to extract basic property info
                price_element = soup.find('span', {'data-test': 'property-price'})
                if price_element:
                    print(f"Price found: {price_element.text}")
                else:
                    print("Price not found in HTML")

                return True
            else:
                print(f"Failed with status code: {response.status_code}")
                return False

        except Exception as e:
            print(f"Error: {e}")
            return False

    def test_selenium_scraping(self, zpid: str):
        """Test Selenium-based web scraping"""
        print("\n=== Testing Selenium Web Scraping ===")

        # Setup Chrome options
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # Run in background
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument(f'user-agent={self.headers["User-Agent"]}')

        try:
            # Initialize driver (requires chromedriver installed)
            driver = webdriver.Chrome(options=chrome_options)
            url = f"https://www.zillow.com/homedetails/{zpid}_zpid/"

            print(f"Loading URL: {url}")
            driver.get(url)

            # Wait for page to load
            wait = WebDriverWait(driver, 10)

            # Try to find price element
            try:
                price_element = wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '[data-test="property-price"]'))
                )
                print(f"Price found: {price_element.text}")

                # Try to get address
                address_element = driver.find_element(By.CSS_SELECTOR, 'h1')
                if address_element:
                    print(f"Address: {address_element.text}")

                return True

            except Exception as e:
                print(f"Could not find elements: {e}")

                # Save screenshot for debugging
                driver.save_screenshot("debug_screenshot.png")
                print("Screenshot saved as debug_screenshot.png")

                return False

        except Exception as e:
            print(f"Selenium error: {e}")
            return False

        finally:
            if 'driver' in locals():
                driver.quit()

    def test_zillow_api(self, zpid: str):
        """Test official Zillow API (requires API key)"""
        print("\n=== Testing Zillow API ===")

        api_key = os.getenv('ZILLOW_API_KEY')
        if api_key == 'your_api_key_here' or not api_key:
            print("No valid API key found in .env file")
            print("To use the Zillow API, you need to:")
            print("1. Register at https://www.zillow.com/howto/api/APIOverview.htm")
            print("2. Get an API key")
            print("3. Update the ZILLOW_API_KEY in your .env file")
            return False

        # Note: Zillow's public API has been largely discontinued
        # This is a placeholder for potential future API endpoints
        print("Note: Zillow's public API access is limited")
        print("Consider using alternative real estate APIs like:")
        print("- Rentberry API")
        print("- Realty Mole API")
        print("- RentSpree API")

        return False

    def test_search_endpoint(self, address: str):
        """Test Zillow's search functionality"""
        print("\n=== Testing Search Endpoint ===")

        search_url = "https://www.zillow.com/search/GetSearchPageState.htm"

        params = {
            'searchQueryState': json.dumps({
                'pagination': {},
                'usersSearchTerm': address,
                'mapBounds': {},
                'isListVisible': True,
                'filterState': {
                    'sortSelection': {'value': 'globalrelevanceex'}
                }
            })
        }

        try:
            response = requests.get(search_url, params=params, headers=self.headers)
            print(f"Status Code: {response.status_code}")

            if response.status_code == 200:
                data = response.json()
                if 'searchResults' in data:
                    print("Search results found!")
                    return True

            return False

        except Exception as e:
            print(f"Error: {e}")
            return False


def main():
    """Main test function"""
    print("=== Zillow API Test Suite ===")
    print("This script tests various methods to retrieve property data from Zillow")

    tester = ZillowAPITester()

    # Test with a sample ZPID (Zillow Property ID)
    # You can find a ZPID by looking at any Zillow property URL
    # Example: https://www.zillow.com/homedetails/123-Main-St/12345678_zpid/

    test_zpid = input("\nEnter a Zillow Property ID (ZPID) to test: ")

    if test_zpid:
        # Run all tests
        results = {
            'Direct Request': tester.test_direct_request(test_zpid),
            'Selenium Scraping': tester.test_selenium_scraping(test_zpid),
            'Zillow API': tester.test_zillow_api(test_zpid)
        }

        # Test search
        address = input("\nEnter a property address to test search: ")
        if address:
            results['Search Endpoint'] = tester.test_search_endpoint(address)

        # Summary
        print("\n=== Test Results Summary ===")
        for test_name, result in results.items():
            status = "✓ PASSED" if result else "✗ FAILED"
            print(f"{test_name}: {status}")

        print("\n=== Recommendations ===")
        if results.get('Selenium Scraping'):
            print("• Selenium scraping works - recommended for detailed data extraction")
        if results.get('Direct Request'):
            print("• Direct requests work - faster but may have limited data")
        if not any(results.values()):
            print("• Consider using alternative real estate data APIs")
            print("• Implement retry logic and proxy rotation")
            print("• Respect robots.txt and terms of service")

    else:
        print("No ZPID provided. Exiting...")


if __name__ == "__main__":
    main()