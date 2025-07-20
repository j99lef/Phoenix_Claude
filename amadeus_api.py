import requests
import logging
import time
from datetime import datetime, timedelta
import config

class AmadeusAPI:
    def __init__(self):
        """Initialize Amadeus API client"""
        self.base_url = "https://api.amadeus.com"
        self.access_token = None
        self.token_expires_at = None
        self.last_request_time = 0
        self.get_access_token()
    
    def get_access_token(self):
        """Get OAuth token for Amadeus API"""
        try:
            url = f"{self.base_url}/v1/security/oauth2/token"
            data = {
                'grant_type': 'client_credentials',
                'client_id': config.AMADEUS_CLIENT_ID,
                'client_secret': config.AMADEUS_CLIENT_SECRET
            }
            
            response = requests.post(url, data=data, timeout=30)
            response.raise_for_status()
            
            token_data = response.json()
            self.access_token = token_data['access_token']
            expires_in = token_data.get('expires_in', 3600)
            self.token_expires_at = datetime.now() + timedelta(seconds=expires_in - 60)
            
            logging.info("Amadeus access token obtained successfully")
            
        except Exception as e:
            logging.error(f"Failed to get Amadeus access token: {e}")
            raise
    
    def ensure_valid_token(self):
        """Ensure we have a valid access token"""
        if not self.access_token or (self.token_expires_at and datetime.now() >= self.token_expires_at):
            self.get_access_token()
    
    def rate_limit(self):
        """Implement rate limiting"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        min_interval = 60.0 / config.AMADEUS_REQUESTS_PER_MINUTE
        
        if time_since_last < min_interval:
            sleep_time = min_interval - time_since_last
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()
    
    def search_flights(self, brief):
        """Search for flights based on brief criteria"""
        self.ensure_valid_token()
        
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        
        try:
            # Parse brief data
            destinations = self.parse_destinations(brief.get('Destinations', ''))
            departure_codes = config.FAMILY_PROFILE['home_airports']
            travel_dates = self.parse_travel_dates(brief.get('Travel_Dates', ''))
            travelers = self.parse_travelers(brief.get('Travelers', ''))
            
            deals = []
            
            for dest_code in destinations:
                for departure_code in departure_codes:
                    for departure_date in travel_dates[:2]:  # Limit to 2 date options
                        self.rate_limit()
                        
                        params = {
                            'originLocationCode': departure_code,
                            'destinationLocationCode': dest_code,
                            'departureDate': departure_date.strftime('%Y-%m-%d'),
                            'adults': travelers['adults'],
                            'children': travelers['children'],
                            'max': 5,  # Limit results per search
                            'currencyCode': 'GBP'
                        }
                        
                        # Add return date if specified
                        if len(travel_dates) > 1:
                            params['returnDate'] = travel_dates[1].strftime('%Y-%m-%d')
                        
                        try:
                            url = f"{self.base_url}/v2/shopping/flight-offers"
                            response = requests.get(url, headers=headers, params=params, timeout=30)
                            
                            if response.status_code == 200:
                                flight_data = response.json()
                                flight_deals = self.format_flight_deals(flight_data, brief)
                                deals.extend(flight_deals)
                                logging.info(f"Found {len(flight_deals)} flights for {departure_code}->{dest_code}")
                            else:
                                logging.warning(f"Amadeus API error {response.status_code}: {response.text}")
                                
                        except requests.exceptions.RequestException as e:
                            logging.error(f"Request error for {departure_code}->{dest_code}: {e}")
                            continue
            
            return deals[:config.MAX_DEALS_PER_SEARCH]  # Limit total deals
            
        except Exception as e:
            logging.error(f"Error searching flights: {e}")
            return []
    
    def search_hotels(self, brief, destination_code, check_in_date, check_out_date):
        """Search for hotels using Amadeus Hotel API"""
        self.ensure_valid_token()
        
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        
        try:
            # First, search for hotels by city
            search_params = {
                'cityCode': destination_code,
                'radius': 20,
                'radiusUnit': 'KM',
                'hotelSource': 'ALL'
            }
            
            self.rate_limit()
            search_url = f"{self.base_url}/v1/reference-data/locations/hotels/by-city"
            search_response = requests.get(search_url, headers=headers, params=search_params, timeout=30)
            
            if search_response.status_code != 200:
                logging.warning(f"Hotel search by city failed: {search_response.text}")
                return []
            
            hotel_search_data = search_response.json()
            hotel_ids = [hotel['hotelId'] for hotel in hotel_search_data.get('data', [])[:10]]  # Get top 10 hotels
            
            if not hotel_ids:
                logging.info(f"No hotels found in {destination_code}")
                return []
            
            # Now get offers for these hotels
            params = {
                'hotelIds': ','.join(hotel_ids),
                'checkInDate': check_in_date.strftime('%Y-%m-%d'),
                'checkOutDate': check_out_date.strftime('%Y-%m-%d'),
                'adults': 2,  # Family default
                'roomQuantity': 1,
                'currency': 'GBP',
                'bestRateOnly': True
            }
            
            self.rate_limit()
            url = f"{self.base_url}/v3/shopping/hotel-offers"
            response = requests.get(url, headers=headers, params=params, timeout=30)
            
            if response.status_code == 200:
                hotel_data = response.json()
                return self.format_hotel_deals(hotel_data, brief, destination_code)
            else:
                logging.warning(f"Hotel API error {response.status_code}: {response.text}")
                return []
                
        except Exception as e:
            logging.error(f"Error searching hotels for {destination_code}: {e}")
            return []
    
    def create_travel_packages(self, brief):
        """Create complete travel packages combining flights and hotels"""
        try:
            # Get flight deals
            flight_deals = self.search_flights(brief)
            
            if not flight_deals:
                logging.info("No flights found, cannot create packages")
                return []
            
            packages = []
            travel_dates = self.parse_travel_dates(brief.get('Travel_Dates', ''))
            
            # Group flights by destination
            flights_by_destination = {}
            for flight in flight_deals:
                dest = flight['destination']
                if dest not in flights_by_destination:
                    flights_by_destination[dest] = []
                flights_by_destination[dest].append(flight)
            
            # Create packages for each destination
            for destination, destination_flights in flights_by_destination.items():
                # Get best flight for this destination
                best_flight = min(destination_flights, key=lambda x: x['total_price'])
                
                # Search for hotels
                check_in = travel_dates[0] if travel_dates else datetime.now() + timedelta(days=30)
                check_out = travel_dates[1] if len(travel_dates) > 1 else check_in + timedelta(days=5)
                
                hotel_deals = self.search_hotels(brief, destination, check_in, check_out)
                
                if hotel_deals:
                    best_hotel = min(hotel_deals, key=lambda x: x['total_price'])
                    
                    # Create package combining flight + hotel
                    package = {
                        'id': f"PKG-{destination}-{best_flight['id'][:8]}",
                        'type': 'package',
                        'destination': destination,
                        'destination_name': self.get_destination_name(destination),
                        'departure_date': best_flight['departure_date'],
                        'return_date': best_flight['return_date'],
                        'duration_nights': (check_out - check_in).days,
                        
                        # Flight details
                        'flight': best_flight,
                        'flight_price': best_flight['total_price'],
                        
                        # Hotel details  
                        'hotel': best_hotel,
                        'hotel_name': best_hotel.get('name', 'Premium Hotel'),
                        'hotel_rating': best_hotel.get('rating', '4+'),
                        'hotel_price': best_hotel['total_price'],
                        'room_type': best_hotel.get('room_type', 'Family Room'),
                        'hotel_amenities': best_hotel.get('amenities', []),
                        
                        # Package totals
                        'total_price': best_flight['total_price'] + best_hotel['total_price'],
                        'currency': best_flight['currency'],
                        'savings': self.calculate_savings(best_flight, best_hotel),
                        
                        'brief_id': brief.get('Brief_ID', ''),
                        'found_at': datetime.now().isoformat()
                    }
                    packages.append(package)
                    logging.info(f"Created package for {destination}: £{package['total_price']}")
            
            return packages
            
        except Exception as e:
            logging.error(f"Error creating travel packages: {e}")
            return []
    
    def format_hotel_deals(self, hotel_data, brief, destination_code):
        """Format hotel API response into standardized format"""
        deals = []
        
        try:
            for hotel in hotel_data.get('data', []):
                hotel_info = hotel['hotel']
                offers = hotel.get('offers', [])
                
                if not offers:
                    continue
                
                best_offer = min(offers, key=lambda x: float(x['price']['total']))
                
                deal = {
                    'id': hotel_info['hotelId'],
                    'type': 'hotel',
                    'name': hotel_info['name'],
                    'destination': destination_code,
                    'rating': hotel_info.get('rating', 4),
                    'total_price': float(best_offer['price']['total']),
                    'currency': best_offer['price']['currency'],
                    'price_per_night': float(best_offer['price']['total']) / max(1, best_offer.get('room', {}).get('typeEstimated', {}).get('beds', 1)),
                    'check_in': best_offer['checkInDate'],
                    'check_out': best_offer['checkOutDate'],
                    'room_type': best_offer['room']['typeEstimated']['category'],
                    'amenities': hotel_info.get('amenities', []),
                    'address': hotel_info.get('address', {}),
                    'brief_id': brief.get('Brief_ID', ''),
                    'found_at': datetime.now().isoformat()
                }
                deals.append(deal)
                
        except Exception as e:
            logging.error(f"Error formatting hotel deals: {e}")
        
        return deals
    
    def get_destination_name(self, code):
        """Convert airport/city codes to readable names"""
        destinations = {
            'BCN': 'Barcelona',
            'VAL': 'Valencia', 
            'VLC': 'Valencia',
            'FCO': 'Rome',
            'ROM': 'Rome',
            'ATH': 'Athens',
            'LCA': 'Cyprus',
            'LIS': 'Lisbon',
            'MAD': 'Madrid',
            'PMI': 'Mallorca'
        }
        return destinations.get(code, code)
    
    def calculate_savings(self, flight, hotel):
        """Calculate potential savings for package deals"""
        # Simple savings calculation - could be enhanced with real pricing data
        individual_total = flight['total_price'] + hotel['total_price']
        package_discount = individual_total * 0.05  # Assume 5% package discount
        return round(package_discount, 2)
    
    def format_flight_deals(self, flight_data, brief):
        """Format Amadeus response into standardized deal format"""
        deals = []
        
        try:
            for offer in flight_data.get('data', []):
                # Extract departure and arrival info
                outbound = offer['itineraries'][0]['segments'][0]
                inbound = offer['itineraries'][1]['segments'][-1] if len(offer['itineraries']) > 1 else None
                
                deal = {
                    'id': offer['id'],
                    'type': 'flight',
                    'origin': outbound['departure']['iataCode'],
                    'destination': outbound['arrival']['iataCode'],
                    'departure_date': outbound['departure']['at'][:10],
                    'departure_time': outbound['departure']['at'][11:16],
                    'return_date': inbound['arrival']['at'][:10] if inbound else None,
                    'return_time': inbound['arrival']['at'][11:16] if inbound else None,
                    'total_price': float(offer['price']['total']),
                    'currency': offer['price']['currency'],
                    'airline': outbound['carrierCode'],
                    'stops': len(offer['itineraries'][0]['segments']) - 1,
                    'duration': offer['itineraries'][0]['duration'],
                    'booking_class': offer['travelerPricings'][0]['fareDetailsBySegment'][0]['class'],
                    'seats_available': offer['numberOfBookableSeats'],
                    'brief_id': brief.get('Brief_ID', ''),
                    'found_at': datetime.now().isoformat()
                }
                deals.append(deal)
                
        except Exception as e:
            logging.error(f"Error formatting flight deals: {e}")
        
        return deals
    
    def parse_destinations(self, destinations_str):
        """Parse destination string into airport codes"""
        if not destinations_str:
            return []
        
        # Simple mapping of common destinations to airport codes
        destination_map = {
            'paris': 'CDG',
            'rome': 'FCO',
            'dubai': 'DXB',
            'new york': 'JFK',
            'amsterdam': 'AMS',
            'barcelona': 'BCN',
            'madrid': 'MAD',
            'berlin': 'BER',
            'prague': 'PRG',
            'vienna': 'VIE',
            'budapest': 'BUD',
            'copenhagen': 'CPH',
            'stockholm': 'ARN',
            'oslo': 'OSL',
            'helsinki': 'HEL',
            'zurich': 'ZUR',
            'geneva': 'GVA',
            'milan': 'MXP',
            'venice': 'VCE',
            'florence': 'FLR',
            'naples': 'NAP',
            'athens': 'ATH',
            'istanbul': 'IST',
            'lisbon': 'LIS',
            'porto': 'OPO',
            'dublin': 'DUB',
            'edinburgh': 'EDI',
            'reykjavik': 'KEF'
        }
        
        destinations = []
        for dest in destinations_str.lower().split(','):
            dest = dest.strip()
            if len(dest) == 3 and dest.isupper():
                # Already an airport code
                destinations.append(dest)
            elif dest in destination_map:
                destinations.append(destination_map[dest])
        
        return destinations
    
    def parse_travel_dates(self, dates_str):
        """Parse travel dates string into datetime objects"""
        if not dates_str:
            # Default to next month
            next_month = datetime.now() + timedelta(days=30)
            return [next_month]
        
        try:
            from dateutil import parser as date_parser
            import re
            
            dates = []
            
            # Handle natural language format like "October 25 - November 2 2025"
            if ' - ' in dates_str:
                parts = dates_str.split(' - ')
                if len(parts) == 2:
                    try:
                        # Parse first date
                        start_date = date_parser.parse(parts[0].strip())
                        # Parse second date, may need year from first date
                        end_part = parts[1].strip()
                        if not re.search(r'\d{4}', end_part):  # No year in end date
                            end_part += f' {start_date.year}'
                        end_date = date_parser.parse(end_part)
                        
                        dates.append(start_date)
                        dates.append(end_date)
                        return dates
                    except:
                        pass
            
            # Try to parse as a single date first
            try:
                single_date = datetime.strptime(dates_str.strip(), '%Y-%m-%d')
                dates.append(single_date)
                return dates
            except:
                pass
                
            # Handle format like "2025-08-15 to 2025-08-22"
            if ' to ' in dates_str:
                parts = dates_str.split(' to ')
                if len(parts) == 2:
                    dates.append(datetime.strptime(parts[0].strip(), '%Y-%m-%d'))
                    dates.append(datetime.strptime(parts[1].strip(), '%Y-%m-%d'))
                    return dates
            
            return dates
            
        except Exception as e:
            logging.error(f"Error parsing travel dates '{dates_str}': {e}")
            # Fallback to October 2025 for the TB-OCT-2025 brief
            fallback_date = datetime(2025, 10, 25)
            return [fallback_date]
    
    def parse_travelers(self, travelers_str):
        """Parse travelers string into adult/child counts"""
        try:
            # Default family configuration
            result = {'adults': 2, 'children': 2, 'total': 4}
            
            if not travelers_str:
                return result
            
            # Parse format like "2 adults, 2 children" or "4 people"
            travelers_str = travelers_str.lower()
            
            if 'adult' in travelers_str:
                import re
                adults_match = re.search(r'(\d+)\s*adult', travelers_str)
                if adults_match:
                    result['adults'] = int(adults_match.group(1))
            
            if 'child' in travelers_str:
                import re
                children_match = re.search(r'(\d+)\s*child', travelers_str)
                if children_match:
                    result['children'] = int(children_match.group(1))
            
            if 'people' in travelers_str:
                import re
                people_match = re.search(r'(\d+)\s*people', travelers_str)
                if people_match:
                    total = int(people_match.group(1))
                    if total == 5:
                        # Including Tabitha
                        result = {'adults': 2, 'children': 3, 'total': 5}
                    else:
                        result['total'] = total
            
            result['total'] = result['adults'] + result['children']
            return result
            
        except Exception as e:
            logging.error(f"Error parsing travelers '{travelers_str}': {e}")
            return {'adults': 2, 'children': 2, 'total': 4}
