"""UK Holidays and School Term integration service."""
import requests
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional

class UKHolidaysService:
    """Service to fetch UK bank holidays and manage school term data."""
    
    BANK_HOLIDAYS_API = "https://www.gov.uk/bank-holidays.json"
    
    def __init__(self):
        self.bank_holidays_cache = None
        self.cache_expiry = None
    
    def get_bank_holidays(self, year: Optional[int] = None) -> Dict:
        """Fetch UK bank holidays from gov.uk API."""
        try:
            # Check cache (valid for 24 hours)
            if (self.bank_holidays_cache and self.cache_expiry and 
                datetime.now() < self.cache_expiry):
                logging.info("Using cached bank holidays data")
                return self.bank_holidays_cache
            
            # Fetch fresh data
            response = requests.get(self.BANK_HOLIDAYS_API, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            self.bank_holidays_cache = data
            self.cache_expiry = datetime.now() + timedelta(hours=24)
            
            logging.info("Fetched fresh bank holidays data from gov.uk")
            return data
            
        except Exception as e:
            logging.error(f"Failed to fetch bank holidays: {e}")
            return self._get_fallback_bank_holidays()
    
    def get_england_bank_holidays(self, year: Optional[int] = None) -> List[Dict]:
        """Get England and Wales bank holidays for specified year."""
        data = self.get_bank_holidays()
        england_holidays = data.get('england-and-wales', {}).get('events', [])
        
        if year:
            # Filter by year
            year_str = str(year)
            england_holidays = [
                h for h in england_holidays 
                if h.get('date', '').startswith(year_str)
            ]
        
        return england_holidays
    
    def get_school_term_suggestions(self, council_key: str) -> Dict:
        """Get school term suggestions for a council."""
        # This would integrate with our school database
        from ..static.uk_schools_database import UK_LOCAL_AUTHORITIES
        
        council_data = UK_LOCAL_AUTHORITIES.get(council_key, {})
        holidays = council_data.get('holidays', {})
        inset_days = council_data.get('insetDays', [])
        
        # Combine with bank holidays
        bank_holidays = self.get_england_bank_holidays(2025)
        
        return {
            'council': council_data.get('name', 'Unknown Council'),
            'school_holidays': holidays,
            'inset_days': inset_days,
            'bank_holidays': bank_holidays,
            'travel_opportunities': self._identify_travel_opportunities(holidays, inset_days, bank_holidays)
        }
    
    def _identify_travel_opportunities(self, school_holidays: Dict, inset_days: List, bank_holidays: List) -> List[Dict]:
        """Identify good travel opportunities based on holiday patterns."""
        opportunities = []
        
        # INSET day opportunities
        for inset in inset_days:
            if inset.get('opportunity') == 'extended-weekend':
                opportunities.append({
                    'type': 'extended_weekend',
                    'date': inset['date'],
                    'description': f"INSET day on {inset['date']} creates extended weekend",
                    'ideal_for': 'City breaks, short trips'
                })
        
        # Half-term opportunities
        for holiday_name, holiday_data in school_holidays.items():
            if 'half-term' in holiday_name:
                opportunities.append({
                    'type': 'half_term',
                    'start': holiday_data['start'],
                    'end': holiday_data['end'],
                    'description': f"{holiday_name.replace('-', ' ').title()}",
                    'ideal_for': 'Week-long family holidays'
                })
        
        # Main holiday opportunities
        for holiday_name, holiday_data in school_holidays.items():
            if holiday_data.get('type') == 'main-holiday':
                opportunities.append({
                    'type': 'main_holiday',
                    'start': holiday_data['start'],
                    'end': holiday_data['end'],
                    'description': f"{holiday_name.replace('-', ' ').title()}",
                    'ideal_for': 'Extended family trips, long-haul destinations'
                })
        
        return opportunities
    
    def _get_fallback_bank_holidays(self) -> Dict:
        """Fallback bank holidays data if API fails."""
        return {
            'england-and-wales': {
                'events': [
                    {'title': 'New Year\'s Day', 'date': '2025-01-01'},
                    {'title': 'Good Friday', 'date': '2025-04-18'},
                    {'title': 'Easter Monday', 'date': '2025-04-21'},
                    {'title': 'Early May bank holiday', 'date': '2025-05-05'},
                    {'title': 'Spring bank holiday', 'date': '2025-05-26'},
                    {'title': 'Summer bank holiday', 'date': '2025-08-25'},
                    {'title': 'Christmas Day', 'date': '2025-12-25'},
                    {'title': 'Boxing Day', 'date': '2025-12-26'}
                ]
            }
        }

# Global service instance
uk_holidays_service = UKHolidaysService()