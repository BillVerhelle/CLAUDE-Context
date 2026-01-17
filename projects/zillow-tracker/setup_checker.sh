#!/bin/bash

# Zillow Property Tracker Setup Checker
# This script verifies that all dependencies and configurations are properly set up

echo "===================================="
echo "Zillow Property Tracker Setup Check"
echo "===================================="
echo ""

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python version
echo "Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    echo -e "${GREEN}✓${NC} Python 3 found: $PYTHON_VERSION"
else
    echo -e "${RED}✗${NC} Python 3 not found. Please install Python 3.7 or higher"
    exit 1
fi

echo ""

# Check required Python packages
echo "Checking Python packages..."
PACKAGES=("requests" "schedule" "python-dotenv" "beautifulsoup4" "selenium" "pandas" "lxml")

for package in "${PACKAGES[@]}"; do
    if python3 -c "import $package" 2>/dev/null; then
        VERSION=$(python3 -c "import $package; print($package.__version__)" 2>/dev/null || echo "installed")
        echo -e "${GREEN}✓${NC} $package: $VERSION"
    else
        echo -e "${YELLOW}⚠${NC} $package: not installed (run: pip3 install $package)"
    fi
done

echo ""

# Check for required files
echo "Checking required files..."
FILES=("zillow_property_tracker.py" "requirements.txt" ".env" "test_api.py")

for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        echo -e "${GREEN}✓${NC} $file exists"
    else
        echo -e "${RED}✗${NC} $file not found"
    fi
done

echo ""

# Check .env configuration
echo "Checking .env configuration..."
if [ -f ".env" ]; then
    source .env

    if [ "$ZILLOW_API_KEY" == "your_api_key_here" ] || [ -z "$ZILLOW_API_KEY" ]; then
        echo -e "${YELLOW}⚠${NC} ZILLOW_API_KEY not configured in .env"
    else
        echo -e "${GREEN}✓${NC} ZILLOW_API_KEY configured"
    fi

    if [ "$EMAIL_FROM" == "your_email@gmail.com" ] || [ -z "$EMAIL_FROM" ]; then
        echo -e "${YELLOW}⚠${NC} Email settings not configured in .env"
    else
        echo -e "${GREEN}✓${NC} Email settings configured"
    fi
else
    echo -e "${RED}✗${NC} .env file not found"
fi

echo ""

# Check for ChromeDriver (for Selenium)
echo "Checking ChromeDriver for Selenium..."
if command -v chromedriver &> /dev/null; then
    CHROME_VERSION=$(chromedriver --version 2>&1 | awk '{print $2}')
    echo -e "${GREEN}✓${NC} ChromeDriver found: $CHROME_VERSION"
else
    echo -e "${YELLOW}⚠${NC} ChromeDriver not found (needed for Selenium web scraping)"
    echo "  Install with: brew install chromedriver (on macOS)"
fi

echo ""

# Check for data files
echo "Checking data files..."
if [ -f "property_data.json" ]; then
    PROPERTY_COUNT=$(python3 -c "import json; data=json.load(open('property_data.json')); print(len(data))" 2>/dev/null || echo "0")
    echo -e "${GREEN}✓${NC} property_data.json exists with $PROPERTY_COUNT properties"
else
    echo -e "${YELLOW}⚠${NC} property_data.json not found (will be created on first run)"
fi

if [ -f "property_report.csv" ]; then
    echo -e "${GREEN}✓${NC} property_report.csv exists"
else
    echo -e "${YELLOW}⚠${NC} property_report.csv not found (will be created on export)"
fi

echo ""

# Test basic functionality
echo "Testing basic functionality..."
python3 -c "from zillow_property_tracker import ZillowPropertyTracker; tracker = ZillowPropertyTracker(); print('✓ Property tracker can be imported and initialized')" 2>/dev/null

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓${NC} Basic import test passed"
else
    echo -e "${RED}✗${NC} Failed to import property tracker"
fi

echo ""
echo "===================================="
echo "Setup Check Complete!"
echo "===================================="

# Summary
echo ""
echo "Next steps:"
echo "1. Install missing packages: pip3 install -r requirements.txt"
echo "2. Configure your .env file with actual API keys and settings"
echo "3. Run the demo: python3 demo.py"
echo "4. Start tracking properties: python3 zillow_property_tracker.py"