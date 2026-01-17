#!/usr/bin/env python3
"""
Demo script to show the Zillow Property Tracker functionality
"""

from zillow_property_tracker import ZillowPropertyTracker


def main():
    """Demonstrate the property tracker with sample data"""

    print("=== Zillow Property Tracker Demo ===\n")

    # Create tracker instance
    tracker = ZillowPropertyTracker()

    # Add sample properties
    print("Adding sample properties...\n")

    # Property 1
    tracker.add_property(
        zpid="12345678",
        address="123 Main St, Nashville, TN 37201",
        price=450000,
        bedrooms=3,
        bathrooms=2.5,
        sqft=2200
    )

    # Property 2
    tracker.add_property(
        zpid="87654321",
        address="456 Oak Ave, Nashville, TN 37203",
        price=525000,
        bedrooms=4,
        bathrooms=3,
        sqft=2800
    )

    # Property 3
    tracker.add_property(
        zpid="11223344",
        address="789 Elm Dr, Nashville, TN 37205",
        price=380000,
        bedrooms=2,
        bathrooms=2,
        sqft=1600
    )

    # Simulate price update for property 1
    print("\nUpdating price for first property...")
    tracker.update_price("12345678", 455000)

    # Display summary
    tracker.display_summary()

    # Export to CSV
    print("\nExporting data to CSV...")
    tracker.export_to_csv("property_report.csv")

    print("\nDemo complete! Check property_data.json and property_report.csv for the data.")


if __name__ == "__main__":
    main()