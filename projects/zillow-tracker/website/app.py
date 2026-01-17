#!/usr/bin/env python3
"""
Flask web application for Zillow Property Tracker
"""

from flask import Flask, render_template, request, jsonify, send_file
import json
import os
import sys
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from zillow_property_tracker import ZillowPropertyTracker

app = Flask(__name__)
tracker = ZillowPropertyTracker(data_file='../property_data.json')


@app.route('/')
def index():
    """Home page with property dashboard"""
    return render_template('index.html')


@app.route('/api/properties')
def get_properties():
    """API endpoint to get all properties"""
    properties_list = []
    for zpid, data in tracker.properties.items():
        property_info = {
            'zpid': zpid,
            'address': data['address'],
            'bedrooms': data['bedrooms'],
            'bathrooms': data['bathrooms'],
            'sqft': data['sqft'],
            'date_added': data['date_added'],
            'price_history': data['price_history']
        }

        if data['price_history']:
            property_info['current_price'] = data['price_history'][-1]['price']
            property_info['initial_price'] = data['price_history'][0]['price']
            property_info['price_change'] = property_info['current_price'] - property_info['initial_price']
            property_info['percent_change'] = (property_info['price_change'] / property_info['initial_price'] * 100) if property_info['initial_price'] > 0 else 0

        properties_list.append(property_info)

    return jsonify(properties_list)


@app.route('/api/add_property', methods=['POST'])
def add_property():
    """API endpoint to add a new property"""
    data = request.json
    tracker.add_property(
        zpid=data['zpid'],
        address=data['address'],
        price=float(data['price']),
        bedrooms=int(data['bedrooms']),
        bathrooms=float(data['bathrooms']),
        sqft=int(data['sqft'])
    )
    return jsonify({'status': 'success', 'message': 'Property added successfully'})


@app.route('/api/update_price', methods=['POST'])
def update_price():
    """API endpoint to update property price"""
    data = request.json
    tracker.update_price(data['zpid'], float(data['price']))
    return jsonify({'status': 'success', 'message': 'Price updated successfully'})


@app.route('/api/export')
def export_csv():
    """Export data to CSV"""
    filename = 'property_export.csv'
    tracker.export_to_csv(filename)
    return send_file(filename, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
