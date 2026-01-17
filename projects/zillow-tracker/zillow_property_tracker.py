#!/usr/bin/env python3
"""
Zillow Property Tracker
A script to track and monitor property listings on Zillow
"""

import requests
import json
import csv
from datetime import datetime
from typing import Dict, List, Optional
import os


class ZillowPropertyTracker:
    """Track properties from Zillow listings"""

    def __init__(self, data_file: str = "property_data.json"):
        self.data_file = data_file
        self.properties = self.load_properties()

    def load_properties(self) -> Dict:
        """Load existing property data from file"""
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                return json.load(f)
        return {}

    def save_properties(self):
        """Save property data to file"""
        with open(self.data_file, 'w') as f:
            json.dump(self.properties, f, indent=2)

    def add_property(self, zpid: str, address: str, price: float,
                     bedrooms: int, bathrooms: float, sqft: int):
        """Add a new property to track"""
        if zpid not in self.properties:
            self.properties[zpid] = {
                'address': address,
                'price_history': [],
                'bedrooms': bedrooms,
                'bathrooms': bathrooms,
                'sqft': sqft,
                'date_added': datetime.now().isoformat()
            }

        # Add current price to history
        self.properties[zpid]['price_history'].append({
            'price': price,
            'date': datetime.now().isoformat()
        })

        self.save_properties()
        print(f"Property {address} added/updated successfully")

    def update_price(self, zpid: str, new_price: float):
        """Update the price for an existing property"""
        if zpid in self.properties:
            self.properties[zpid]['price_history'].append({
                'price': new_price,
                'date': datetime.now().isoformat()
            })
            self.save_properties()
            print(f"Price updated for {self.properties[zpid]['address']}")
        else:
            print(f"Property with ZPID {zpid} not found")

    def get_price_change(self, zpid: str) -> Optional[float]:
        """Calculate price change for a property"""
        if zpid in self.properties and len(self.properties[zpid]['price_history']) >= 2:
            history = self.properties[zpid]['price_history']
            initial_price = history[0]['price']
            current_price = history[-1]['price']
            return current_price - initial_price
        return None

    def export_to_csv(self, filename: str = "property_report.csv"):
        """Export property data to CSV"""
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['ZPID', 'Address', 'Current Price', 'Initial Price',
                         'Price Change', 'Bedrooms', 'Bathrooms', 'Sqft', 'Date Added']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for zpid, data in self.properties.items():
                if data['price_history']:
                    current_price = data['price_history'][-1]['price']
                    initial_price = data['price_history'][0]['price']
                    price_change = current_price - initial_price
                else:
                    current_price = initial_price = price_change = 0

                writer.writerow({
                    'ZPID': zpid,
                    'Address': data['address'],
                    'Current Price': current_price,
                    'Initial Price': initial_price,
                    'Price Change': price_change,
                    'Bedrooms': data['bedrooms'],
                    'Bathrooms': data['bathrooms'],
                    'Sqft': data['sqft'],
                    'Date Added': data['date_added']
                })
        print(f"Data exported to {filename}")

    def display_summary(self):
        """Display summary of tracked properties"""
        print("\n=== Property Tracking Summary ===\n")
        for zpid, data in self.properties.items():
            print(f"Address: {data['address']}")
            print(f"ZPID: {zpid}")
            print(f"Bedrooms: {data['bedrooms']} | Bathrooms: {data['bathrooms']} | Sqft: {data['sqft']}")

            if data['price_history']:
                current_price = data['price_history'][-1]['price']
                initial_price = data['price_history'][0]['price']
                price_change = current_price - initial_price
                percent_change = (price_change / initial_price) * 100 if initial_price > 0 else 0

                print(f"Current Price: ${current_price:,.2f}")
                print(f"Initial Price: ${initial_price:,.2f}")
                print(f"Price Change: ${price_change:,.2f} ({percent_change:+.2f}%)")

            print("-" * 50)


def main():
    """Main function to demonstrate usage"""
    tracker = ZillowPropertyTracker()

    while True:
        print("\n=== Zillow Property Tracker ===")
        print("1. Add/Update Property")
        print("2. Update Property Price")
        print("3. View Summary")
        print("4. Export to CSV")
        print("5. Exit")

        choice = input("\nSelect an option (1-5): ")

        if choice == '1':
            zpid = input("Enter Zillow Property ID (ZPID): ")
            address = input("Enter property address: ")
            price = float(input("Enter current price: "))
            bedrooms = int(input("Enter number of bedrooms: "))
            bathrooms = float(input("Enter number of bathrooms: "))
            sqft = int(input("Enter square footage: "))

            tracker.add_property(zpid, address, price, bedrooms, bathrooms, sqft)

        elif choice == '2':
            zpid = input("Enter Zillow Property ID (ZPID): ")
            new_price = float(input("Enter new price: "))
            tracker.update_price(zpid, new_price)

        elif choice == '3':
            tracker.display_summary()

        elif choice == '4':
            filename = input("Enter CSV filename (or press Enter for default): ")
            if filename:
                tracker.export_to_csv(filename)
            else:
                tracker.export_to_csv()

        elif choice == '5':
            print("Exiting... Goodbye!")
            break

        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()