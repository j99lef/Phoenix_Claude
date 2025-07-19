#!/usr/bin/env python3
"""Check if deals are being found and stored in the database."""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app
from travel_aigent.models import db, Deal, TravelBrief
from datetime import datetime

def check_deals_status():
    """Check the status of deals in the database."""
    with app.app_context():
        print("\n=== Deal System Status Check ===\n")
        
        # Check if deals table exists
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        
        if 'deals' not in tables:
            print("❌ Deals table does not exist!")
            return
        
        # Count total deals
        total_deals = Deal.query.count()
        print(f"Total deals in database: {total_deals}")
        
        if total_deals == 0:
            print("❌ No deals found in database!")
            print("\nPossible reasons:")
            print("  1. Amadeus API is not searching for deals")
            print("  2. API credentials might be invalid")
            print("  3. Deal search is not being triggered")
            print("  4. Deals are found but not saved to database")
        else:
            # Show recent deals
            recent_deals = Deal.query.order_by(Deal.created_at.desc()).limit(5).all()
            print(f"\n✅ Found {total_deals} deals. Recent deals:")
            
            for deal in recent_deals:
                print(f"\nDeal ID: {deal.id}")
                print(f"  Destination: {deal.destination}")
                print(f"  Price: {deal.currency} {deal.price}")
                print(f"  Type: {deal.type}")
                print(f"  Provider: {deal.provider}")
                print(f"  Created: {deal.created_at}")
                print(f"  Brief ID: {deal.brief_id}")
        
        # Check briefs
        print("\n=== Travel Briefs Status ===")
        total_briefs = TravelBrief.query.count()
        print(f"Total briefs in database: {total_briefs}")
        
        if total_briefs > 0:
            recent_briefs = TravelBrief.query.order_by(TravelBrief.created_at.desc()).limit(3).all()
            print("\nRecent briefs:")
            for brief in recent_briefs:
                print(f"\nBrief ID: {brief.id}")
                print(f"  User ID: {brief.user_id}")
                print(f"  Destination: {brief.destination}")
                print(f"  Status: {brief.status}")
                print(f"  Created: {brief.created_at}")
                
                # Count deals for this brief
                brief_deals = Deal.query.filter_by(brief_id=brief.id).count()
                print(f"  Deals found: {brief_deals}")

def test_amadeus_credentials():
    """Test if Amadeus credentials are set."""
    print("\n=== Amadeus Configuration ===")
    
    import config
    
    if hasattr(config, 'AMADEUS_CLIENT_ID') and config.AMADEUS_CLIENT_ID:
        print(f"✅ AMADEUS_CLIENT_ID is set: {config.AMADEUS_CLIENT_ID[:10]}...")
    else:
        print("❌ AMADEUS_CLIENT_ID is not set!")
    
    if hasattr(config, 'AMADEUS_CLIENT_SECRET') and config.AMADEUS_CLIENT_SECRET:
        print(f"✅ AMADEUS_CLIENT_SECRET is set: {config.AMADEUS_CLIENT_SECRET[:5]}...")
    else:
        print("❌ AMADEUS_CLIENT_SECRET is not set!")

if __name__ == "__main__":
    check_deals_status()
    test_amadeus_credentials()
    
    print("\n=== Summary ===")
    print("If no deals are found, the issue is likely:")
    print("1. Amadeus API credentials not set in environment")
    print("2. Deal search not being triggered when briefs are created")
    print("3. API search failing but errors not being logged")
    print("\nCheck travel_agent.log for error messages.")