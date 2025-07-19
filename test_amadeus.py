#!/usr/bin/env python
"""Test Amadeus API connection"""
import os
import sys

# Set test credentials
os.environ['AMADEUS_CLIENT_ID'] = 'xNIE44DrMfsiRPXpLCXG7EzjOxntDGAf'
os.environ['AMADEUS_CLIENT_SECRET'] = 'GYJGY2FW7pkohsQx'

# Import after setting env vars
from amadeus_api import AmadeusAPI
from datetime import datetime, timedelta

def test_amadeus_connection():
    """Test if we can connect to Amadeus API"""
    print("Testing Amadeus API connection...")
    
    try:
        # Initialize API
        api = AmadeusAPI()
        print("✅ Successfully authenticated with Amadeus API!")
        print(f"   Access token obtained: {api.access_token[:20]}...")
        
        # Test a simple flight search
        print("\nTesting flight search...")
        departure_date = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
        
        deals = api.search_flights(
            origin='LON',
            destination='PAR',
            departure_date=departure_date,
            adults=2,
            max_price=500
        )
        
        if deals:
            print(f"✅ Found {len(deals)} flight deals!")
            print(f"   Example: {deals[0]['title']} - £{deals[0]['price']}")
        else:
            print("ℹ️  No deals found for the test search (LON to PAR)")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_amadeus_connection()
    sys.exit(0 if success else 1)