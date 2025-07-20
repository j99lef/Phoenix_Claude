#!/usr/bin/env python3
"""
Test script to verify Amadeus API connection and functionality
"""

import os
import sys
import logging
from datetime import datetime, timedelta

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def test_amadeus_connection():
    """Test the Amadeus API connection and basic functionality"""
    
    print("\n=== TravelAiGent Amadeus API Test ===\n")
    
    # Check environment variables
    print("1. Checking environment variables...")
    amadeus_id = os.getenv("AMADEUS_CLIENT_ID", "")
    amadeus_secret = os.getenv("AMADEUS_CLIENT_SECRET", "")
    
    if not amadeus_id or not amadeus_secret:
        print("❌ AMADEUS_CLIENT_ID and AMADEUS_CLIENT_SECRET not found in environment")
        print("\nTo fix this:")
        print("1. Sign up for a free Amadeus API account at: https://developers.amadeus.com/")
        print("2. Create a new app in your Amadeus dashboard")
        print("3. Copy your Client ID and Client Secret")
        print("4. Edit the .env file and add your credentials:")
        print("   AMADEUS_CLIENT_ID=your-actual-client-id")
        print("   AMADEUS_CLIENT_SECRET=your-actual-client-secret")
        print("5. Run this test again\n")
        return False
    else:
        print("✅ Amadeus credentials found in environment")
    
    # Try to initialize Amadeus API
    print("\n2. Testing Amadeus API initialization...")
    try:
        from amadeus_api import AmadeusAPI
        api = AmadeusAPI()
        print("✅ Amadeus API initialized successfully")
        print(f"   Access token obtained: {'Yes' if api.access_token else 'No'}")
    except Exception as e:
        print(f"❌ Failed to initialize Amadeus API: {e}")
        return False
    
    # Test a simple flight search
    print("\n3. Testing flight search functionality...")
    try:
        # Create a test brief
        test_brief = {
            'Brief_ID': 'TEST-001',
            'Departure_Location': 'London',
            'Destinations': 'Paris, Rome',
            'Travel_Dates': f"{(datetime.now() + timedelta(days=60)).strftime('%Y-%m-%d')}",
            'Travelers': '2 adults, 2 children',
            'Budget_Min': 2000,
            'Budget_Max': 5000,
            'Accommodation_Type': '4-5 star hotels',
            'AI_Instructions': 'Family-friendly destinations with good weather'
        }
        
        print(f"   Searching flights from London to Paris/Rome...")
        print(f"   Date: {test_brief['Travel_Dates']}")
        
        flights = api.search_flights(test_brief)
        
        if flights:
            print(f"✅ Found {len(flights)} flights!")
            for i, flight in enumerate(flights[:3]):  # Show first 3
                print(f"\n   Flight {i+1}:")
                print(f"   - Route: {flight.get('origin')} → {flight.get('destination')}")
                print(f"   - Date: {flight.get('departure_date')}")
                print(f"   - Price: {flight.get('currency')} {flight.get('total_price')}")
                print(f"   - Airline: {flight.get('airline')}")
        else:
            print("⚠️  No flights found (this might be normal if searching far in advance)")
    except Exception as e:
        print(f"❌ Flight search failed: {e}")
        return False
    
    # Test hotel search
    print("\n4. Testing hotel search functionality...")
    try:
        hotels = api.search_hotels(
            test_brief, 
            'PAR',  # Paris
            datetime.now() + timedelta(days=60),
            datetime.now() + timedelta(days=65)
        )
        
        if hotels:
            print(f"✅ Found {len(hotels)} hotels in Paris!")
            for i, hotel in enumerate(hotels[:2]):  # Show first 2
                print(f"\n   Hotel {i+1}:")
                print(f"   - Name: {hotel.get('name')}")
                print(f"   - Rating: {hotel.get('rating')} stars")
                print(f"   - Price: {hotel.get('currency')} {hotel.get('total_price')}")
        else:
            print("⚠️  No hotels found")
    except Exception as e:
        print(f"⚠️  Hotel search not critical: {e}")
    
    # Test the full travel agent flow
    print("\n5. Testing Travel Agent integration...")
    try:
        from travel_agent import TravelAgent
        agent = TravelAgent()
        
        if agent.amadeus:
            print("✅ Travel Agent connected to Amadeus API")
            
            # Test processing a brief
            print("\n   Processing test brief...")
            agent.process_travel_brief(test_brief)
            print("✅ Brief processed successfully")
            
            # Check stats
            print(f"\n   Stats:")
            print(f"   - Total deals found: {agent.get_total_deals_count()}")
            print(f"   - Notifications sent: {agent.get_notifications_count()}")
        else:
            print("❌ Travel Agent failed to connect to Amadeus API")
            print("   The system will use mock data instead")
    except Exception as e:
        print(f"❌ Travel Agent test failed: {e}")
    
    print("\n=== Test Complete ===\n")
    return True

if __name__ == "__main__":
    # Load environment variables from .env file
    from dotenv import load_dotenv
    load_dotenv()
    
    test_amadeus_connection()