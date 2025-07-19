#!/usr/bin/env python3
"""Add database saving functionality to travel agent."""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def add_database_saving_to_travel_agent():
    """Add a method to save deals to database in travel_agent.py"""
    
    # The method to add to travel_agent.py
    database_save_method = '''
    def save_deal_to_database(self, deal_data, brief_dict, analysis=None):
        """Save a deal to the database"""
        try:
            from travel_aigent.models import db, Deal, TravelBrief
            from datetime import datetime
            
            # Get the brief from database
            brief_id = brief_dict.get('Brief_ID')
            if not brief_id:
                logging.error("No brief ID provided")
                return
                
            brief = TravelBrief.query.get(brief_id)
            if not brief:
                logging.error(f"Brief {brief_id} not found in database")
                return
            
            # Parse deal data based on type
            if deal_data.get('type') == 'flight':
                deal = Deal(
                    brief_id=brief.id,
                    user_id=brief.user_id,
                    title=f"Flight to {deal_data.get('destination', 'Unknown')}",
                    description=f"{deal_data.get('airline', 'Airline')} flight from {deal_data.get('origin')} to {deal_data.get('destination')}",
                    price=float(deal_data.get('total_price', 0)),
                    original_price=float(deal_data.get('total_price', 0)) * 1.2,  # Estimate original
                    currency=deal_data.get('currency', 'GBP'),
                    provider=deal_data.get('airline', 'Unknown'),
                    booking_url=deal_data.get('booking_url', '#'),
                    destination=deal_data.get('destination', ''),
                    departure_date=datetime.fromisoformat(deal_data.get('departure_date')) if deal_data.get('departure_date') else None,
                    return_date=datetime.fromisoformat(deal_data.get('return_date')) if deal_data.get('return_date') else None,
                    airline=deal_data.get('airline'),
                    flight_duration=deal_data.get('duration'),
                    type='flight',
                    match_score=int(analysis.get('score', 0) * 10) if analysis else 70,
                    status='active'
                )
            elif 'hotel' in deal_data.get('type', '').lower():
                deal = Deal(
                    brief_id=brief.id,
                    user_id=brief.user_id,
                    title=deal_data.get('hotel_name', 'Hotel Deal'),
                    description=deal_data.get('description', 'Hotel accommodation'),
                    price=float(deal_data.get('total_price', 0)),
                    original_price=float(deal_data.get('total_price', 0)) * 1.15,
                    currency=deal_data.get('currency', 'GBP'),
                    provider=deal_data.get('provider', 'Unknown'),
                    booking_url=deal_data.get('booking_url', '#'),
                    destination=deal_data.get('destination', ''),
                    hotel_name=deal_data.get('hotel_name'),
                    hotel_rating=deal_data.get('rating'),
                    type='hotel',
                    match_score=int(analysis.get('score', 0) * 10) if analysis else 70,
                    status='active'
                )
            else:  # Package or other
                deal = Deal(
                    brief_id=brief.id,
                    user_id=brief.user_id,
                    title=deal_data.get('title', f"Travel Package to {deal_data.get('destination', 'Unknown')}"),
                    description=deal_data.get('description', 'Complete travel package'),
                    price=float(deal_data.get('total_price', 0)),
                    original_price=float(deal_data.get('original_price', deal_data.get('total_price', 0))),
                    currency=deal_data.get('currency', 'GBP'),
                    provider=deal_data.get('provider', 'Unknown'),
                    booking_url=deal_data.get('booking_url', '#'),
                    destination=deal_data.get('destination', ''),
                    type='package',
                    match_score=int(analysis.get('score', 0) * 10) if analysis else 70,
                    status='active'
                )
            
            # Save to database
            db.session.add(deal)
            db.session.commit()
            
            logging.info(f"Saved deal to database: {deal.title} (ID: {deal.id})")
            
            # Send notification if enabled
            if brief.user and analysis and analysis.get('score', 0) >= 8:
                try:
                    from travel_aigent.services.notifications import notification_service
                    notification_service.send_deal_notification(brief.user, deal, brief)
                except Exception as e:
                    logging.error(f"Failed to send notification: {e}")
                    
        except Exception as e:
            logging.error(f"Error saving deal to database: {e}")
            db.session.rollback()
'''
    
    print("Add this method to travel_agent.py after the __init__ method:")
    print("=" * 80)
    print(database_save_method)
    print("=" * 80)
    print("\nThen modify the process_travel_brief method to call self.save_deal_to_database(deal, brief, analysis)")
    print("after analyzing each deal.")

if __name__ == "__main__":
    add_database_saving_to_travel_agent()
    
    print("\n\nALTERNATIVELY, create a separate service that:")
    print("1. Monitors for new deals from Amadeus")
    print("2. Saves them to the database")
    print("3. This keeps travel_agent.py focused on finding deals")
    print("\nThe issue is that travel_agent.py only logs to Google Sheets, not the database!")