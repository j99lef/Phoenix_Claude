import logging
import time
from datetime import datetime, timedelta
from sheets_handler import SheetsHandler
from amadeus_api import AmadeusAPI
from openai_analyzer import OpenAIAnalyzer
from telegram_notifier import TelegramNotifier
import config

class TravelAgent:
    def __init__(self):
        """Initialize the Travel Agent with all required services"""
        self.sheets = SheetsHandler()
        
        # Initialize services with error handling
        try:
            self.amadeus = AmadeusAPI()
        except Exception as e:
            logging.warning(f"Amadeus API initialization failed: {e}. Will use mock data.")
            self.amadeus = None
            
        try:
            self.ai_analyzer = OpenAIAnalyzer()
        except Exception as e:
            logging.warning(f"OpenAI analyzer initialization failed: {e}. Will use mock analysis.")
            self.ai_analyzer = None
            
        try:
            self.telegram = TelegramNotifier()
        except Exception as e:
            logging.warning(f"Telegram notifier initialization failed: {e}. Will log notifications.")
            self.telegram = None
            
        self.last_check_time = None
        self.stats = {
            'total_deals_found': 0,
            'notifications_sent': 0,
            'searches_completed': 0
        }
        
    def run_initial_check(self):
        """Run initial check and remove the one-time schedule"""
        import schedule
        logging.info("Running initial deal search...")
        self.run_deal_search()
        # Clear the initial check schedule
        schedule.clear('initial')
        
    def run_deal_search(self):
        """Main execution flow for deal searching"""
        try:
            self.last_check_time = datetime.now()
            logging.info("Starting travel deal search cycle...")
            
            # Get active travel briefs
            active_briefs = self.sheets.get_active_briefs()
            
            if not active_briefs:
                logging.info("No active travel briefs found")
                return
                
            logging.info(f"Processing {len(active_briefs)} active travel briefs")
            
            for brief in active_briefs:
                try:
                    self.process_travel_brief(brief)
                    time.sleep(2)  # Rate limiting between briefs
                except Exception as e:
                    logging.error(f"Error processing brief {brief.get('Brief_ID', 'Unknown')}: {e}")
                    continue
                    
            self.stats['searches_completed'] += 1
            logging.info(f"Deal search cycle completed. Total searches: {self.stats['searches_completed']}")
            
        except Exception as e:
            logging.error(f"Error in deal search cycle: {e}")
    
    def save_deal_to_database(self, deal_data, brief_dict, analysis=None):
        """Save a deal to the database"""
        try:
            from travel_aigent.models import db, Deal, TravelBrief
            from datetime import datetime
            import app
            
            with app.app.app_context():
                # Get the brief from database
                brief_id = brief_dict.get('Brief_ID')
                if not brief_id:
                    logging.error("No brief ID provided")
                    return
                    
                brief = TravelBrief.query.get(int(brief_id))
                if not brief:
                    logging.error(f"Brief {brief_id} not found in database")
                    return
                
                # Parse deal data based on type
                deal_type = deal_data.get('type', 'package')
                
                if 'flight' in deal_type:
                    deal = Deal(
                        brief_id=brief.id,
                        user_id=brief.user_id,
                        title=f"Flight to {deal_data.get('destination', 'Unknown')}",
                        description=f"{deal_data.get('airline', 'Airline')} flight from {deal_data.get('origin')} to {deal_data.get('destination')}",
                        price=float(deal_data.get('total_price', 0)),
                        original_price=float(deal_data.get('total_price', 0)) * 1.2,
                        currency=deal_data.get('currency', 'GBP'),
                        provider=deal_data.get('airline', 'Amadeus'),
                        booking_url=deal_data.get('booking_url', '#'),
                        destination=deal_data.get('destination', ''),
                        departure_date=datetime.strptime(deal_data.get('departure_date'), '%Y-%m-%d') if deal_data.get('departure_date') else None,
                        return_date=datetime.strptime(deal_data.get('return_date'), '%Y-%m-%d') if deal_data.get('return_date') else None,
                        airline=deal_data.get('airline'),
                        flight_duration=deal_data.get('duration'),
                        type='flight',
                        match_score=int(analysis.get('score', 7) * 10) if analysis else 70,
                        status='active'
                    )
                elif 'hotel' in deal_type:
                    deal = Deal(
                        brief_id=brief.id,
                        user_id=brief.user_id,
                        title=deal_data.get('hotel_name', 'Hotel Deal'),
                        description=deal_data.get('description', 'Hotel accommodation'),
                        price=float(deal_data.get('total_price', 0)),
                        original_price=float(deal_data.get('total_price', 0)) * 1.15,
                        currency=deal_data.get('currency', 'GBP'),
                        provider=deal_data.get('provider', 'Amadeus'),
                        booking_url=deal_data.get('booking_url', '#'),
                        destination=deal_data.get('destination', ''),
                        hotel_name=deal_data.get('hotel_name'),
                        hotel_rating=deal_data.get('rating'),
                        type='hotel',
                        match_score=int(analysis.get('score', 7) * 10) if analysis else 70,
                        status='active'
                    )
                else:  # Package or other
                    deal = Deal(
                        brief_id=brief.id,
                        user_id=brief.user_id,
                        title=deal_data.get('title', f"Travel Package to {deal_data.get('destination', 'Unknown')}"),
                        description=deal_data.get('description', 'Complete travel package with flights and hotel'),
                        price=float(deal_data.get('total_price', 0)),
                        original_price=float(deal_data.get('original_price', deal_data.get('total_price', 0)) * 1.1),
                        currency=deal_data.get('currency', 'GBP'),
                        provider=deal_data.get('provider', 'Amadeus'),
                        booking_url=deal_data.get('booking_url', '#'),
                        destination=deal_data.get('destination', ''),
                        departure_date=datetime.strptime(deal_data.get('departure_date'), '%Y-%m-%d') if deal_data.get('departure_date') else None,
                        return_date=datetime.strptime(deal_data.get('return_date'), '%Y-%m-%d') if deal_data.get('return_date') else None,
                        type='package',
                        match_score=int(analysis.get('score', 7) * 10) if analysis else 70,
                        status='active'
                    )
                
                # Add discount percentage
                if deal.original_price > 0:
                    deal.discount_percentage = int(((deal.original_price - deal.price) / deal.original_price) * 100)
                
                # Save to database
                db.session.add(deal)
                db.session.commit()
                
                logging.info(f"Saved deal to database: {deal.title} (ID: {deal.id})")
                
                # Send notification if high score
                if brief.user and analysis and analysis.get('score', 0) >= 8:
                    try:
                        from travel_aigent.services.notifications import notification_service
                        notification_service.send_deal_notification(brief.user, deal, brief)
                        logging.info(f"Sent notification for high-score deal {deal.id}")
                    except Exception as e:
                        logging.error(f"Failed to send notification: {e}")
                        
        except Exception as e:
            logging.error(f"Error saving deal to database: {e}")
            try:
                db.session.rollback()
            except:
                pass
    
    def process_travel_brief(self, brief):
        """Process individual travel brief"""
        brief_id = brief.get('Brief_ID', 'Unknown')
        logging.info(f"Processing travel brief: {brief_id}")
        
        try:
            # Search for complete travel packages (flights + hotels)
            travel_packages = []
            if self.amadeus:
                travel_packages = self.amadeus.create_travel_packages(brief)
                if not travel_packages:
                    # Fallback to flight-only search if package creation fails
                    flight_deals = self.amadeus.search_flights(brief)
                    travel_packages = [{'type': 'flight_only', **deal} for deal in flight_deals]
            else:
                # Mock data when Amadeus is unavailable
                travel_packages = self._get_mock_flight_deals(brief)
                
            logging.info(f"Found {len(travel_packages)} travel packages for brief {brief_id}")
            
            # Process each package/deal
            for deal in travel_packages:
                try:
                    # Check if we've already processed this deal recently
                    if self.sheets.is_duplicate_deal(deal):
                        continue
                        
                    # Analyze deal with AI
                    if self.ai_analyzer:
                        analysis = self.ai_analyzer.analyze_deal(deal, brief)
                    else:
                        analysis = self._get_mock_analysis(deal)
                    
                    # Log the deal regardless of score
                    self.sheets.log_deal(deal, analysis, brief)
                    self.stats['total_deals_found'] += 1
                    
                    # Save deal to database
                    self.save_deal_to_database(deal, brief, analysis)
                    
                    # Send alert if score is high enough
                    if analysis.get('score', 0) >= config.MIN_SCORE_FOR_ALERT:
                        if self.telegram:
                            self.telegram.send_alert(deal, analysis, brief)
                        else:
                            logging.info(f"Mock notification: High-score deal for {deal.get('destination', 'Unknown')}")
                        self.stats['notifications_sent'] += 1
                        logging.info(f"High-score deal alert sent for {deal.get('destination', 'Unknown')}")
                    
                    time.sleep(1)  # Rate limiting between deal analyses
                    
                except Exception as e:
                    logging.error(f"Error processing deal: {e}")
                    continue
            
            # Update last checked timestamp for this brief
            self.sheets.update_brief_timestamp(brief_id)
            
        except Exception as e:
            logging.error(f"Error processing brief {brief_id}: {e}")
    
    def _get_mock_flight_deals(self, brief):
        """Generate mock flight deals for testing"""
        from datetime import datetime
        
        destinations = brief.get('Destinations', 'Paris').split(',')
        deals = []
        
        for dest in destinations[:2]:  # Limit to 2 destinations
            dest = dest.strip()
            deal = {
                'id': f"MOCK_{dest}_{datetime.now().strftime('%H%M%S')}",
                'type': 'flight',
                'origin': 'LHR',
                'destination': dest.upper()[:3] if len(dest) >= 3 else 'PAR',
                'departure_date': '2025-08-15',
                'departure_time': '08:30',
                'return_date': '2025-08-22',
                'return_time': '18:45',
                'total_price': 450.0 + len(dest) * 10,  # Vary price
                'currency': 'GBP',
                'airline': 'BA',
                'stops': 0,
                'duration': 'PT2H30M',
                'booking_class': 'Economy',
                'seats_available': 9,
                'brief_id': brief.get('Brief_ID', ''),
                'found_at': datetime.now().isoformat()
            }
            deals.append(deal)
        
        return deals
    
    def _get_mock_analysis(self, deal):
        """Generate mock AI analysis for testing"""
        import random
        
        score = random.randint(6, 10)
        recommendations = ['BOOK_NOW', 'WATCH', 'IGNORE']
        
        return {
            'score': score,
            'recommendation': recommendations[0] if score >= 8 else recommendations[1],
            'value_assessment': f"Good value flight to {deal.get('destination', 'destination')}",
            'family_suitability': 'Suitable for family travel with children',
            'key_pros': ['Direct flight', 'Good timing', 'Reasonable price'],
            'key_cons': ['Peak season', 'Limited availability'],
            'action_summary': f"Consider booking this {score}/10 rated deal to {deal.get('destination', 'destination')}"
        }
    
    def get_last_check_time(self):
        """Get the last check time as a string"""
        if self.last_check_time:
            return self.last_check_time.strftime("%Y-%m-%d %H:%M:%S")
        return "Never"
    
    def get_active_briefs_count(self):
        """Get count of active briefs"""
        try:
            briefs = self.sheets.get_active_briefs()
            return len(briefs)
        except:
            return 0
    
    def get_total_deals_count(self):
        """Get total deals found"""
        return self.stats['total_deals_found']
    
    def get_notifications_count(self):
        """Get notifications sent count"""
        return self.stats['notifications_sent']
