"""UK School Holidays Data (2024-2026)"""
from datetime import datetime

UK_SCHOOL_HOLIDAYS = {
    "England": {
        "2024-2025": [
            {"name": "Half-term break", "start": "2024-10-28", "end": "2024-11-01", "type": "half_term"},
            {"name": "Christmas holiday", "start": "2024-12-23", "end": "2025-01-03", "type": "christmas"}
        ],
        "2025": [
            {"name": "Spring Holiday", "start": "2025-02-17", "end": "2025-02-21", "type": "spring_half_term"},
            {"name": "Easter holiday", "start": "2025-04-07", "end": "2025-04-21", "type": "easter"},
            {"name": "May Half Term", "start": "2025-05-26", "end": "2025-05-30", "type": "may_half_term"},
            {"name": "Summer break", "start": "2025-07-22", "end": "2025-08-31", "type": "summer"},
            {"name": "Autumn Holidays", "start": "2025-10-27", "end": "2025-10-31", "type": "autumn_half_term"},
            {"name": "Christmas Holidays", "start": "2025-12-19", "end": "2026-01-05", "type": "christmas"}
        ],
        "2026": [
            {"name": "Spring Holiday", "start": "2026-02-16", "end": "2026-02-20", "type": "spring_half_term"},
            {"name": "Easter Holidays", "start": "2026-03-30", "end": "2026-04-10", "type": "easter"},
            {"name": "May Half Term", "start": "2026-05-25", "end": "2026-05-29", "type": "may_half_term"},
            {"name": "Summer Holidays", "start": "2026-07-20", "end": "2026-09-02", "type": "summer"},
            {"name": "Autumn Holidays", "start": "2026-10-26", "end": "2026-10-30", "type": "autumn_half_term"},
            {"name": "Christmas Holidays", "start": "2026-12-21", "end": "2027-01-01", "type": "christmas"}
        ]
    },
    "Scotland": {
        "2024-2025": [
            {"name": "Mid-term holiday", "start": "2024-10-14", "end": "2024-10-18", "type": "autumn_half_term"},
            {"name": "Christmas holiday", "start": "2024-12-23", "end": "2025-01-03", "type": "christmas"}
        ],
        "2025": [
            {"name": "Spring Holiday", "start": "2025-02-17", "end": "2025-02-20", "type": "spring_half_term"},
            {"name": "Easter holiday", "start": "2025-04-07", "end": "2025-04-18", "type": "easter"},
            {"name": "May Half Term", "start": "2025-05-05", "end": "2025-05-06", "type": "may_half_term"},
            {"name": "Summer holiday", "start": "2025-06-26", "end": "2025-08-19", "type": "summer"},
            {"name": "Autumn Holidays", "start": "2025-10-13", "end": "2025-10-17", "type": "autumn_half_term"},
            {"name": "Christmas Holidays", "start": "2025-12-22", "end": "2026-01-05", "type": "christmas"}
        ],
        "2026": [
            {"name": "Spring Holiday", "start": "2026-02-16", "end": "2026-02-20", "type": "spring_half_term"},
            {"name": "Easter Holidays", "start": "2026-04-03", "end": "2026-04-17", "type": "easter"},
            {"name": "May Half Term", "start": "2026-05-04", "end": "2026-05-06", "type": "may_half_term"},
            {"name": "Summer Holidays", "start": "2026-07-02", "end": "2026-08-12", "type": "summer"},
            {"name": "Autumn Holidays", "start": "2026-10-12", "end": "2026-10-19", "type": "autumn_half_term"},
            {"name": "Christmas Holidays", "start": "2026-12-21", "end": "2027-01-05", "type": "christmas"}
        ]
    },
    "Wales": {
        "2024-2025": [
            {"name": "Autumn half term", "start": "2024-10-28", "end": "2024-11-01", "type": "autumn_half_term"},
            {"name": "Christmas holiday", "start": "2024-12-23", "end": "2025-01-03", "type": "christmas"}
        ],
        "2025": [
            {"name": "Spring half term", "start": "2025-02-24", "end": "2025-02-28", "type": "spring_half_term"},
            {"name": "Easter holiday", "start": "2025-04-14", "end": "2025-04-25", "type": "easter"},
            {"name": "May Half Term", "start": "2025-05-26", "end": "2025-05-30", "type": "may_half_term"},
            {"name": "Summer holiday", "start": "2025-07-21", "end": "2025-09-01", "type": "summer"},
            {"name": "Autumn Holidays", "start": "2025-10-27", "end": "2025-10-31", "type": "autumn_half_term"},
            {"name": "Christmas Holidays", "start": "2025-12-19", "end": "2026-01-05", "type": "christmas"}
        ],
        "2026": [
            {"name": "Spring Holiday", "start": "2026-02-16", "end": "2026-02-20", "type": "spring_half_term"},
            {"name": "Easter Holidays", "start": "2026-03-30", "end": "2026-04-10", "type": "easter"},
            {"name": "May Half Term", "start": "2026-05-25", "end": "2026-05-29", "type": "may_half_term"},
            {"name": "Summer Holidays", "start": "2026-07-20", "end": "2026-09-02", "type": "summer"},
            {"name": "Autumn Holidays", "start": "2026-10-26", "end": "2026-10-30", "type": "autumn_half_term"},
            {"name": "Christmas Holidays", "start": "2026-12-21", "end": "2027-01-01", "type": "christmas"}
        ]
    },
    "Northern Ireland": {
        "2024-2025": [
            {"name": "Halloween", "start": "2024-10-31", "end": "2024-11-01", "type": "autumn_half_term"},
            {"name": "Christmas holiday", "start": "2024-12-23", "end": "2025-01-02", "type": "christmas"}
        ],
        "2025": [
            {"name": "Spring Holidays", "start": "2025-02-13", "end": "2025-02-14", "type": "spring_half_term"},
            {"name": "Easter holiday", "start": "2025-04-17", "end": "2025-04-25", "type": "easter"},
            {"name": "Summer holiday", "start": "2025-07-01", "end": "2025-08-31", "type": "summer"},
            {"name": "Autumn Holidays", "start": "2025-10-30", "end": "2025-10-31", "type": "autumn_half_term"},
            {"name": "Christmas Holidays", "start": "2025-12-22", "end": "2026-01-02", "type": "christmas"}
        ]
    }
}

HOLIDAY_TYPES = {
    "spring_half_term": "Spring Half Term",
    "easter": "Easter Holidays",
    "may_half_term": "May Half Term", 
    "summer": "Summer Break",
    "autumn_half_term": "October Half Term",
    "christmas": "Winter Break"
}

def get_holidays_for_country(country, year=None):
    """Get holidays for a specific country and optionally year"""
    if country not in UK_SCHOOL_HOLIDAYS:
        return []
    
    holidays = []
    country_data = UK_SCHOOL_HOLIDAYS[country]
    
    for year_key, year_holidays in country_data.items():
        if year is None or str(year) in year_key:
            holidays.extend(year_holidays)
    
    return holidays

def get_holiday_by_type(country, holiday_type, year=None):
    """Get specific holiday type for a country"""
    holidays = get_holidays_for_country(country, year)
    return [h for h in holidays if h["type"] == holiday_type]

def get_upcoming_holidays(country, from_date=None):
    """Get upcoming holidays from a specific date"""
    if from_date is None:
        from_date = datetime.now()
    elif isinstance(from_date, str):
        from_date = datetime.strptime(from_date, "%Y-%m-%d")
    
    holidays = get_holidays_for_country(country)
    upcoming = []
    
    for holiday in holidays:
        start_date = datetime.strptime(holiday["start"], "%Y-%m-%d")
        if start_date >= from_date:
            upcoming.append(holiday)
    
    return sorted(upcoming, key=lambda x: x["start"])

def is_school_holiday(country, check_date):
    """Check if a specific date falls within school holidays"""
    if isinstance(check_date, str):
        check_date = datetime.strptime(check_date, "%Y-%m-%d")
    
    holidays = get_holidays_for_country(country)
    
    for holiday in holidays:
        start = datetime.strptime(holiday["start"], "%Y-%m-%d")
        end = datetime.strptime(holiday["end"], "%Y-%m-%d")
        if start <= check_date <= end:
            return True, holiday
    
    return False, None