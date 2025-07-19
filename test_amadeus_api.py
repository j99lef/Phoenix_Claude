#!/usr/bin/env python3
"""Test Amadeus API to verify it's working."""
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set Amadeus credentials from RAILWAY_ENV_VARS.md
os.environ['AMADEUS_CLIENT_ID'] = 'xNIE44DrMfsiRPXpLCXG7EzjOxntDGAf'
os.environ['AMADEUS_CLIENT_SECRET'] = 'GYJGY2FW7pkohsQx'

from amadeus_api import AmadeusAPI
from datetime import datetime, timedelta
import json

def test_amadeus_connection():
    """Test basic Amadeus API connection."""
    print("\n=== Testing Amadeus API Connection ===\n")
    
    try:
        # Initialize API
        api = AmadeusAPI()
        print(f"✅ Successfully initialized Amadeus API")
        print(f"   Access token: {api.access_token[:20]}...")
        print(f"   Token expires at: {api.token_expires_at}")
        
        return api
    except Exception as e:
        print(f"❌ Failed to initialize Amadeus API: {e}")
        return None

def test_flight_search(api):
    """Test flight search functionality."""
    print("\n=== Testing Flight Search ===\n")
    
    if not api:
        print("❌ No API instance available")
        return
    
    try:
        # Search for flights from London to Barcelona
        departure_date = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
        return_date = (datetime.now() + timedelta(days=37)).strftime('%Y-%m-%d')
        
        print(f"Searching flights:")
        print(f"  From: LON (London)")
        print(f"  To: BCN (Barcelona)")
        print(f"  Departure: {departure_date}")
        print(f"  Return: {return_date}")
        print(f"  Adults: 2")
        
        offers = api.search_flights(
            origin='LON',
            destination='BCN',
            departure_date=departure_date,
            return_date=return_date,
            adults=2,
            max_results=3
        )
        
        if offers:
            print(f"\n✅ Found {len(offers)} flight offers!")
            for i, offer in enumerate(offers, 1):
                print(f"\nOffer {i}:")
                print(f"  Price: {offer['price']['currency']} {offer['price']['total']}")
                print(f"  Airlines: {', '.join(offer['airlines'])}")
                print(f"  Outbound: {offer['outbound_departure']} → {offer['outbound_arrival']}")
                print(f"  Return: {offer['return_departure']} → {offer['return_arrival']}")
        else:
            print("❌ No flight offers found")
            
    except Exception as e:
        print(f"❌ Flight search failed: {e}")

def test_hotel_search(api):
    """Test hotel search functionality."""
    print("\n=== Testing Hotel Search ===\n")
    
    if not api:
        print("❌ No API instance available")
        return
    
    try:
        print(f"Searching hotels in Barcelona...")
        
        hotels = api.search_hotels_by_city(
            city_code='BCN',
            max_results=3
        )
        
        if hotels:
            print(f"\n✅ Found {len(hotels)} hotels!")
            for i, hotel in enumerate(hotels, 1):
                print(f"\nHotel {i}:")
                print(f"  Name: {hotel.get('name', 'Unknown')}")
                print(f"  Hotel ID: {hotel.get('hotelId', 'Unknown')}")
                if 'geoCode' in hotel:
                    print(f"  Location: {hotel['geoCode'].get('latitude', 'N/A')}, {hotel['geoCode'].get('longitude', 'N/A')}")
        else:
            print("❌ No hotels found")
            
    except Exception as e:
        print(f"❌ Hotel search failed: {e}")

def check_api_in_travel_agent():
    """Check if API is being used in travel_agent.py"""
    print("\n=== Checking Travel Agent Integration ===\n")
    
    try:
        from travel_agent import TravelAgent
        agent = TravelAgent()
        
        if hasattr(agent, 'amadeus') and agent.amadeus:
            print("✅ Amadeus API is initialized in TravelAgent")
            print(f"   API instance: {type(agent.amadeus)}")
        else:
            print("❌ Amadeus API is NOT initialized in TravelAgent")
            
    except Exception as e:
        print(f"❌ Failed to check TravelAgent: {e}")

if __name__ == "__main__":
    # Test Amadeus connection
    api = test_amadeus_connection()
    
    if api:
        # Test flight search
        test_flight_search(api)
        
        # Test hotel search
        test_hotel_search(api)
    
    # Check travel agent integration
    check_api_in_travel_agent()
    
    print("\n=== Test Complete ===\n")