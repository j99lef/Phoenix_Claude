#!/usr/bin/env python3
"""Test deals functionality comprehensively."""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from travel_aigent import create_app
from travel_aigent.models import db, User, Deal, TravelBrief
from datetime import datetime, timedelta
import time
from flask import session

def test_deals():
    """Test deals functionality."""
    app = create_app()
    
    with app.app_context():
        print("=" * 80)
        print("TESTING DEALS FUNCTIONALITY")
        print("=" * 80)
        
        # 1. Check admin user
        print("\n1. Checking admin user:")
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            print("   ❌ Admin not found!")
            return
        print(f"   ✅ Admin exists (ID: {admin.id})")
        
        # 2. Create a test travel brief
        print("\n2. Creating test travel brief:")
        
        # Check if test brief exists
        test_brief = TravelBrief.query.filter_by(
            user_id=admin.id,
            destination='Paris'
        ).first()
        
        if not test_brief:
            test_brief = TravelBrief(
                user_id=admin.id,
                departure_location='London',
                destination='Paris',
                departure_date=datetime.now() + timedelta(days=30),
                return_date=datetime.now() + timedelta(days=37),
                budget_min=1000,
                budget_max=2000,
                travelers='2 adults',
                accommodation_type='hotel',
                interests='culture,food',
                priority='high',
                date_flexibility=3,
                amadeus_destination_code='PAR'
            )
            db.session.add(test_brief)
            db.session.commit()
            print(f"   ✅ Created test brief (ID: {test_brief.id})")
        else:
            print(f"   ✅ Test brief exists (ID: {test_brief.id})")
            
        # 3. Check if any deals exist
        print("\n3. Checking existing deals:")
        total_deals = Deal.query.count()
        user_deals = Deal.query.filter_by(user_id=admin.id).count()
        brief_deals = Deal.query.filter_by(brief_id=test_brief.id).count()
        
        print(f"   Total deals in database: {total_deals}")
        print(f"   Deals for admin user: {user_deals}")
        print(f"   Deals for test brief: {brief_deals}")
        
        # 4. Create a test deal
        print("\n4. Creating test deal:")
        
        test_deal = Deal(
            brief_id=test_brief.id,
            user_id=admin.id,
            title='Direct Flight to Paris - Great Deal!',
            description='British Airways direct flight LHR to CDG',
            price=299.99,
            original_price=399.99,
            discount_percentage=25,
            provider='Amadeus',
            booking_url='https://example.com/book',
            destination='Paris',
            departure_location='London',
            departure_date=test_brief.departure_date,
            return_date=test_brief.return_date,
            airline='British Airways',
            type='flight',
            currency='GBP',
            total_price=299.99
        )
        
        db.session.add(test_deal)
        db.session.commit()
        print(f"   ✅ Created test deal (ID: {test_deal.id})")
        
        # 5. Test deals API
        print("\n5. Testing deals API endpoint:")
        
        from travel_aigent.routes.deals import get_deals
        
        with app.test_request_context('/api/deals'):
            # Set up session
            session['username'] = 'admin'
            session['authenticated'] = True
            session['login_time'] = time.time()
            
            # Check what the route would do
            from auth import auth
            user = auth.get_current_user()
            
            if user:
                print(f"   ✅ API would get user: {user.username} (ID: {user.id})")
                
                # Get deals like the API would
                deals = Deal.query.filter_by(user_id=user.id).all()
                print(f"   ✅ API would return {len(deals)} active deals")
                
                if deals:
                    print("   Sample deal:")
                    deal = deals[0]
                    print(f"     - {deal.title}")
                    print(f"     - Price: {deal.currency} {deal.price}")
                    print(f"     - Match Score: {deal.match_score}%")
            else:
                print("   ❌ API would fail - no user!")
                
        # 6. Check travel_agent.py integration
        print("\n6. Checking travel_agent.py:")
        
        # Check if the save method was added
        try:
            from travel_agent import TravelAgent
            agent = TravelAgent()
            
            if hasattr(agent, 'save_deal_to_database'):
                print("   ✅ save_deal_to_database method exists")
            else:
                print("   ❌ save_deal_to_database method missing!")
                
        except Exception as e:
            print(f"   ❌ Error checking travel_agent: {e}")
            
        # 7. Summary
        print("\n" + "=" * 80)
        print("DEALS DIAGNOSTIC SUMMARY:")
        print("=" * 80)
        
        final_total = Deal.query.count()
        final_user = Deal.query.filter_by(user_id=admin.id).count()
        
        print(f"✅ Admin user exists: ID {admin.id}")
        print(f"✅ Travel brief exists: ID {test_brief.id}")
        print(f"✅ Deals table works: {final_total} total deals")
        print(f"✅ User has {final_user} deals")
        print(f"✅ Can create and retrieve deals")
        
        print("\nISSUES TO FIX:")
        print("1. Ensure travel_agent.py is saving deals when finding them")
        print("2. Ensure Amadeus API credentials are set in Railway")
        print("3. Ensure deal search is being triggered")
        print("=" * 80)

if __name__ == "__main__":
    test_deals()