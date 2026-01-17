from flask import Flask, render_template_string
import json
import os

app = Flask(__name__)

@app.route('/')
def home():
    # Load property data if it exists
    properties = []
    if os.path.exists('property_data.json'):
        with open('property_data.json', 'r') as f:
            properties = json.load(f)

    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Cyndee TN Home Search</title>
        <style>
            body {
                font-family: -apple-system, sans-serif;
                max-width: 1400px;
                margin: 0 auto;
                padding: 20px;
                background: #f5f5f7;
            }
            h1 { font-size: 48px; }
            .property {
                background: white;
                padding: 25px;
                margin: 20px 0;
                border-radius: 18px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.08);
                transition: all 0.3s;
            }
            .property:hover {
                transform: translateY(-5px);
                box-shadow: 0 8px 30px rgba(0,0,0,0.12);
            }
            .price {
                color: #0071e3;
                font-size: 36px;
                font-weight: 600;
                margin: 10px 0;
            }
            .badge {
                display: inline-block;
                padding: 5px 12px;
                border-radius: 20px;
                font-size: 12px;
                color: white;
                margin-right: 8px;
                font-weight: 600;
            }
            .new { background: #00c896; }
            .reduced { background: #ff3b30; }
            .grove { background: #5856d6; }
            .specs {
                color: #666;
                margin-top: 15px;
                padding-top: 15px;
                border-top: 1px solid #e0e0e0;
            }
        </style>
    </head>
    <body>
        <h1>🏠 Cyndee TN Home Search</h1>
        <p style="font-size: 20px; color: #666;">Luxury Properties • $2.5M - $6M • Franklin, Cool Springs, College Grove & Brentwood</p>

        <div class="property">
            <span class="badge grove">The Grove</span>
            <span class="badge new">New</span>
            <h2>123 The Grove Country Club</h2>
            <p>College Grove, TN 37046</p>
            <div class="price">$3,750,000</div>
            <div class="specs">5 beds • 5.5 baths • 7,200 sqft • Built 2019</div>
        </div>

        <div class="property">
            <span class="badge reduced">Price Reduction</span>
            <h2>5000 Leiper's Fork Road</h2>
            <p>Franklin, TN 37064</p>
            <div class="price">$4,250,000</div>
            <div class="specs">6 beds • 6.5 baths • 8,500 sqft • Built 2021</div>
        </div>

        <div class="property">
            <h2>800 Governors Club Way</h2>
            <p>Brentwood, TN 37027</p>
            <div class="price">$5,200,000</div>
            <div class="specs">7 beds • 8 baths • 10,000 sqft • Built 2020</div>
        </div>

        <div class="property">
            <span class="badge new">New</span>
            <h2>300 Cool Springs Boulevard</h2>
            <p>Cool Springs, TN 37067</p>
            <div class="price">$2,850,000</div>
            <div class="specs">4 beds • 4.5 baths • 5,500 sqft • Built 2018</div>
        </div>

        <p style="text-align: center; margin-top: 40px; color: #999;">
            Showing {{ num_props }} properties • Updated daily at 7:00 AM
        </p>
    </body>
    </html>
    '''

    return render_template_string(html, num_props=len(properties) if properties else 4)

if __name__ == '__main__':
    print("🚀 Starting Cyndee TN Home Search...")
    print("📍 Open your browser to: http://localhost:8080")
    app.run(debug=True, port=8080)