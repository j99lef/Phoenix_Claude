#!/usr/bin/env python3
"""Manually trigger deal search for existing briefs."""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set Amadeus credentials
os.environ['AMADEUS_CLIENT_ID'] = 'xNIE44DrMfsiRPXpLCXG7EzjOxntDGAf'
os.environ['AMADEUS_CLIENT_SECRET'] = 'GYJGY2FW7pkohsQx'

from app import app
from travel_aigent.models import db, TravelBrief, Deal
from travel_agent import TravelAgent
import logging

def trigger_deal_search_for_user_briefs():
    """Trigger deal search for user briefs that have no deals."""
    with app.app_context():
        print("\n=== Triggering Deal Search ===\n")
        
        # Get briefs without deals
        from sqlalchemy import func
        briefs_without_deals = db.session.query(TravelBrief).outerjoin(Deal).group_by(TravelBrief.id).having(func.count(Deal.id) == 0).all()
        
        if not briefs_without_deals:
            print("All briefs already have deals!")
            return
        
        print(f"Found {len(briefs_without_deals)} briefs without deals")
        
        # Initialize travel agent
        try:
            agent = TravelAgent()
            print("✅ Travel agent initialized with Amadeus API")
        except Exception as e:
            print(f"❌ Failed to initialize travel agent: {e}")
            return
        
        # Process each brief
        for brief in briefs_without_deals:
            print(f"\nProcessing Brief ID {brief.id}:")
            print(f"  User ID: {brief.user_id}")
            print(f"  Destination: {brief.destination}")
            print(f"  Budget: £{brief.budget_min} - £{brief.budget_max}")
            
            # Convert to format expected by travel agent
            brief_dict = {
                'Brief_ID': str(brief.id),
                'Departure_Location': brief.departure_location,
                'Destinations': brief.destination,
                'Travelers': brief.travelers or "2 adults, 2 children",
                'Budget_Min': brief.budget_min,
                'Budget_Max': brief.budget_max,
                'Accommodation_Type': brief.accommodation_type,
                'AI_Instructions': brief.interests or "",
                'Trip_Duration': f"{brief.trip_length} days" if brief.trip_length else "7 days"
            }
            
            try:
                print("  Searching for deals...")
                agent.process_travel_brief(brief_dict)
                
                # Check if deals were found
                new_deals = Deal.query.filter_by(brief_id=brief.id).count()
                print(f"  ✅ Found {new_deals} deals for this brief")
                
            except Exception as e:
                print(f"  ❌ Error searching deals: {e}")
                logging.error(f"Deal search error for brief {brief.id}: {e}")

def show_deals_summary():
    """Show summary of deals after search."""
    with app.app_context():
        print("\n=== Deals Summary ===\n")
        
        total_deals = Deal.query.count()
        print(f"Total deals in database: {total_deals}")
        
        # Group by brief
        from sqlalchemy import func
        brief_deals = db.session.query(
            TravelBrief.id,
            TravelBrief.destination,
            func.count(Deal.id).label('deal_count')
        ).join(Deal).group_by(TravelBrief.id).all()
        
        if brief_deals:
            print("\nDeals by brief:")
            for brief_id, destination, count in brief_deals:
                print(f"  Brief {brief_id} ({destination}): {count} deals")

if __name__ == "__main__":
    print("Setting up Amadeus credentials...")
    print(f"Client ID: {os.environ.get('AMADEUS_CLIENT_ID', 'NOT SET')}")
    print(f"Client Secret: {os.environ.get('AMADEUS_CLIENT_SECRET', 'NOT SET')[:5]}...")
    
    trigger_deal_search_for_user_briefs()
    show_deals_summary()
    
    print("\n✅ Deal search triggered. Check the application to see if deals appear.")