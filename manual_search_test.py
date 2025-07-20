#!/usr/bin/env python3
"""
Manual script to trigger a search for testing
"""
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import app
from travel_aigent.models import db, TravelBrief, SearchActivity
from travel_agent import TravelAgent
import logging

def run_manual_search(brief_id):
    """Manually trigger a search for a specific brief"""
    with app.app_context():
        try:
            # Get the brief
            brief = TravelBrief.query.get(brief_id)
            if not brief:
                print(f"Brief {brief_id} not found!")
                return
            
            print(f"Found brief: {brief.destination} (ID: {brief.id})")
            
            # Convert to format expected by travel agent
            brief_dict = {
                'Brief_ID': str(brief.id),
                'Destinations': brief.destination,
                'Departure_Location': brief.departure_location,
                'Travel_Dates': f"{brief.departure_date.strftime('%Y-%m-%d')} to {brief.return_date.strftime('%Y-%m-%d') if brief.return_date else ''}",
                'Budget_Max': brief.budget_max,
                'Travelers': brief.travelers,
                'Trip_Duration': brief.trip_length,
                'AI_Instructions': brief.interests
            }
            
            # Initialize travel agent
            agent = TravelAgent()
            print(f"Travel agent initialized - Amadeus: {agent.amadeus is not None}")
            
            # Process the brief
            print(f"Starting search for brief {brief_id}...")
            agent.process_travel_brief(brief_dict)
            
            # Check for search activities
            activities = SearchActivity.query.filter_by(brief_id=brief_id).all()
            print(f"\nSearch activities created: {len(activities)}")
            for activity in activities:
                print(f"  - {activity.search_type} ({activity.status}): {activity.results_found} results")
            
        except Exception as e:
            logging.error(f"Error in manual search: {e}", exc_info=True)
            print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        brief_id = int(sys.argv[1])
        print(f"Running manual search for brief ID: {brief_id}")
        run_manual_search(brief_id)
    else:
        # List available briefs
        with app.app_context():
            briefs = TravelBrief.query.filter_by(status='active').all()
            if briefs:
                print("Available active briefs:")
                for brief in briefs:
                    print(f"  ID {brief.id}: {brief.destination} - {brief.departure_date}")
                print(f"\nUsage: python3 {sys.argv[0]} <brief_id>")
            else:
                print("No active briefs found!")