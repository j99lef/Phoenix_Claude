"""Create sample deals for testing"""
from datetime import datetime, timedelta
from travel_aigent import create_app
from travel_aigent.models import db, Deal, TravelBrief, User

def create_sample_deals():
    app = create_app()
    
    with app.app_context():
        # Get or create test user
        user = User.query.filter_by(username='demo').first()
        if not user:
            from argon2 import PasswordHasher
            ph = PasswordHasher()
            user = User(
                username='demo',
                email='demo@travelaigent.com',
                password_hash=ph.hash('demo'),
                first_name='Demo',
                last_name='User'
            )
            db.session.add(user)
            db.session.commit()
            print("Created demo user")
        
        # Get or create test brief
        brief = TravelBrief.query.first()
        if not brief:
            brief = TravelBrief(
                user_id=user.id,
                departure_location='London',
                destination='Barcelona',
                departure_date=datetime.now() + timedelta(days=30),
                return_date=datetime.now() + timedelta(days=37),
                travelers='2 Adults',
                budget_min=1000,
                budget_max=3000,
                accommodation_type='5-star hotel',
                interests='Luxury travel, cultural experiences'
            )
            db.session.add(brief)
            db.session.commit()
            print("Created test brief")
        
        # Create sample deals
        deals = [
            {
                'title': 'Barcelona Luxury Escape',
                'description': 'Experience the best of Barcelona with flights and 5-star accommodation',
                'destination': 'BCN',
                'departure_location': 'LON',
                'departure_date': datetime.now() + timedelta(days=30),
                'return_date': datetime.now() + timedelta(days=37),
                'airline': 'British Airways',
                'hotel_name': 'Hotel Arts Barcelona',
                'hotel_rating': 5,
                'total_price': 2450.00,
                'price': 2450.00,
                'original_price': 3200.00,
                'discount_percentage': 23.4,
                'type': 'package',
                'accommodation_type': '5-star hotel',
                'provider': 'Expedia',
                'booking_url': 'https://www.expedia.co.uk/Hotel-Search?destination=Barcelona&startDate=2025-08-25&endDate=2025-09-01&rooms=1&adults=2'
            },
            {
                'title': 'Valencia Beach Holiday',
                'description': 'Relax on the Mediterranean coast with direct flights and beachfront hotel',
                'destination': 'VLC',
                'departure_location': 'LON',
                'departure_date': datetime.now() + timedelta(days=45),
                'return_date': datetime.now() + timedelta(days=52),
                'airline': 'Ryanair',
                'hotel_name': 'Las Arenas Balneario Resort',
                'hotel_rating': 5,
                'total_price': 1899.00,
                'price': 1899.00,
                'original_price': 2400.00,
                'discount_percentage': 20.9,
                'type': 'package',
                'accommodation_type': 'beach resort',
                'provider': 'Booking.com',
                'booking_url': 'https://www.booking.com/searchresults.html?dest_id=-390625&dest_type=city&checkin=2025-09-10&checkout=2025-09-17'
            },
            {
                'title': 'Rome Cultural Weekend',
                'description': 'Discover ancient Rome with guided tours included',
                'destination': 'FCO',
                'departure_location': 'LON',
                'departure_date': datetime.now() + timedelta(days=14),
                'return_date': datetime.now() + timedelta(days=17),
                'airline': 'Alitalia',
                'hotel_name': 'Hotel de Russie',
                'hotel_rating': 5,
                'total_price': 1350.00,
                'price': 1350.00,
                'original_price': 1600.00,
                'discount_percentage': 15.6,
                'type': 'package',
                'accommodation_type': 'luxury hotel',
                'provider': 'TUI',
                'booking_url': 'https://www.tui.co.uk/destinations/europe/italy/rome/holidays-rome.html'
            }
        ]
        
        for deal_data in deals:
            deal = Deal(
                brief_id=brief.id,
                user_id=user.id,
                **deal_data
            )
            db.session.add(deal)
        
        db.session.commit()
        print(f"Created {len(deals)} sample deals")

if __name__ == '__main__':
    create_sample_deals()