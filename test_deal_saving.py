#!/usr/bin/env python3
"""Test script to verify deals are being saved to database."""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime
from travel_agent import TravelAgent

def test_deal_saving():
    """Test if deals are being saved to database."""
    print("Testing deal saving functionality...")
    
    # Create a mock brief
    test_brief = {
        'Brief_ID': '1',
        'Destinations': 'Paris,Rome',
        'Start_Date': '2025-08-01',
        'End_Date': '2025-08-15',
        'Budget': '2000',
        'Travelers': '2 adults',
        'Status': 'Active'
    }
    
    # Create a mock deal
    test_deal = {
        'id': 'TEST_DEAL_001',
        'type': 'flight',
        'origin': 'LHR',
        'destination': 'CDG',
        'departure_date': '2025-08-01',
        'departure_time': '10:00',
        'return_date': '2025-08-08',
        'return_time': '18:00',
        'total_price': 350.0,
        'currency': 'GBP',
        'airline': 'British Airways',
        'stops': 0,
        'duration': 'PT1H30M',
        'booking_class': 'Economy',
        'seats_available': 5,
        'found_at': datetime.now().isoformat()
    }
    
    # Create a mock analysis
    test_analysis = {
        'score': 8.5,
        'recommendation': 'BOOK_NOW',
        'value_assessment': 'Excellent value for Paris trip',
        'family_suitability': 'Great for couples',
        'key_pros': ['Direct flight', 'Good timing', 'Great price'],
        'key_cons': ['Peak season'],
        'action_summary': 'Highly recommended deal for your Paris trip'
    }
    
    try:
        # Initialize travel agent
        agent = TravelAgent()
        
        # Test the save method
        print("\nTesting save_deal_to_database method...")
        agent.save_deal_to_database(test_deal, test_brief, test_analysis)
        
        print("\n✅ Deal saving method called successfully!")
        print("\nTo verify deals are saved:")
        print("1. Run: python check_deals.py")
        print("2. Check the web interface deals page")
        print("3. Check database directly")
        
    except Exception as e:
        print(f"\n❌ Error testing deal saving: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_deal_saving()