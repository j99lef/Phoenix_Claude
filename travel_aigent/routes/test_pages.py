"""Test pages to verify functionality."""
from flask import Blueprint, render_template, jsonify, request, session
from auth import require_auth, auth
from ..models import db, User, UserSchool, Deal, TravelBrief
import json
from datetime import datetime, timedelta

bp = Blueprint('test_pages', __name__)

@bp.route("/schools/simple")
@require_auth
def schools_simple():
    """Simple schools management page."""
    return render_template("schools_simple.html")

@bp.route("/test")
@require_auth
def test_dashboard():
    """Test dashboard showing all functionality status."""
    return render_template("test_dashboard.html")

@bp.route("/test/schools")
@require_auth
def test_schools():
    """Test page for schools functionality."""
    user = auth.get_current_user()
    schools = []
    people = []
    error = None
    
    if user:
        schools = UserSchool.query.filter_by(user_id=user.id).all()
        # Get user's people (children) - need to load the relationship
        from ..models import Person
        people = Person.query.filter_by(user_id=user.id).all()
        # Add people to user object for template
        user.people = people
    else:
        error = "No user found in session"
        
    return render_template("test_schools.html", 
                         user=user, 
                         schools=schools,
                         people=people,
                         error=error)

@bp.route("/test/deals")
@require_auth  
def test_deals():
    """Test page for deals functionality."""
    user = auth.get_current_user()
    deals = []
    briefs = []
    error = None
    
    if user:
        deals = Deal.query.filter_by(user_id=user.id).all()
        briefs = TravelBrief.query.filter_by(user_id=user.id).all()
    else:
        error = "No user found in session"
        
    return render_template("test_deals.html",
                         user=user,
                         deals=deals, 
                         briefs=briefs,
                         error=error)

@bp.route("/test/api/status")
@require_auth
def test_api_status():
    """API endpoint to test all functionality."""
    results = {
        "timestamp": datetime.now().isoformat(),
        "session": dict(session),
        "tests": {}
    }
    
    # Test 1: Authentication
    try:
        user = auth.get_current_user()
        if user:
            results["tests"]["auth"] = {
                "status": "✅ PASS",
                "user_id": user.id,
                "username": user.username,
                "message": f"User authenticated: {user.username} (ID: {user.id})"
            }
        else:
            results["tests"]["auth"] = {
                "status": "❌ FAIL", 
                "message": "get_current_user() returned None"
            }
    except Exception as e:
        results["tests"]["auth"] = {
            "status": "❌ FAIL",
            "error": str(e)
        }
    
    # Test 2: Database
    try:
        user_count = User.query.count()
        admin = User.query.filter_by(username='admin').first()
        results["tests"]["database"] = {
            "status": "✅ PASS",
            "total_users": user_count,
            "admin_exists": admin is not None,
            "admin_id": admin.id if admin else None
        }
    except Exception as e:
        results["tests"]["database"] = {
            "status": "❌ FAIL",
            "error": str(e)
        }
    
    # Test 3: Schools API
    try:
        if user:
            schools = UserSchool.query.filter_by(user_id=user.id).all()
            results["tests"]["schools"] = {
                "status": "✅ PASS",
                "count": len(schools),
                "schools": [s.to_dict() for s in schools]
            }
        else:
            results["tests"]["schools"] = {
                "status": "❌ FAIL",
                "message": "No authenticated user"
            }
    except Exception as e:
        results["tests"]["schools"] = {
            "status": "❌ FAIL", 
            "error": str(e)
        }
    
    # Test 4: Deals API
    try:
        if user:
            deals = Deal.query.filter_by(user_id=user.id).all()
            results["tests"]["deals"] = {
                "status": "✅ PASS",
                "count": len(deals),
                "deals": [{"id": d.id, "title": d.title, "price": d.price} for d in deals]
            }
        else:
            results["tests"]["deals"] = {
                "status": "❌ FAIL",
                "message": "No authenticated user"
            }
    except Exception as e:
        results["tests"]["deals"] = {
            "status": "❌ FAIL",
            "error": str(e)
        }
    
    return jsonify(results)

@bp.route("/test/api/create-test-data", methods=["POST"])
@require_auth
def create_test_data():
    """Create test data for verification."""
    user = auth.get_current_user()
    if not user:
        return jsonify({"error": "No authenticated user"}), 401
        
    created = {}
    
    # Create test school
    try:
        test_school = UserSchool(
            user_id=user.id,
            school_key='test-council-' + str(datetime.now().timestamp()),
            school_name='Test Council',
            school_type='council',
            region='London',
            country='England',
            is_primary=True
        )
        db.session.add(test_school)
        db.session.commit()
        created["school"] = test_school.to_dict()
    except Exception as e:
        created["school"] = {"error": str(e)}
    
    # Create test brief
    try:
        test_brief = TravelBrief(
            user_id=user.id,
            departure_location='London',
            destination='Test Destination',
            departure_date=datetime.now() + timedelta(days=30),
            return_date=datetime.now() + timedelta(days=37),
            travelers='2 adults',
            budget_min=1000,
            budget_max=2000,
            accommodation_type='hotel'
        )
        db.session.add(test_brief)
        db.session.commit()
        
        # Create test deal
        test_deal = Deal(
            brief_id=test_brief.id,
            user_id=user.id,
            title='Test Deal - Direct Flight',
            description='Test deal created for verification',
            price=299.99,
            original_price=399.99,
            discount_percentage=25,
            provider='Test Provider',
            booking_url='#',
            destination='Test Destination',
            departure_location='London',
            departure_date=test_brief.departure_date,
            return_date=test_brief.return_date,
            type='flight'
        )
        db.session.add(test_deal)
        db.session.commit()
        
        created["brief"] = {"id": test_brief.id, "destination": test_brief.destination}
        created["deal"] = {"id": test_deal.id, "title": test_deal.title, "price": test_deal.price}
    except Exception as e:
        created["brief"] = {"error": str(e)}
        created["deal"] = {"error": str(e)}
    
    return jsonify({
        "message": "Test data created",
        "created": created
    })