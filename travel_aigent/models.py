"""Database models for Travel AiGent system"""
import os
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

# Initialize db without explicit model class to avoid registry conflicts
db = SQLAlchemy()


class User(db.Model):
    """User model for profile and account management"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # Profile Information
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    whatsapp_number = db.Column(db.String(20))  # For WhatsApp notifications
    
    # Travel Preferences
    home_airports = db.Column(db.Text)  # JSON string of preferred airports
    preferred_airlines = db.Column(db.Text)  # JSON string
    dietary_restrictions = db.Column(db.Text)
    travel_style = db.Column(db.String(50))  # luxury, budget, adventure, etc.
    
    # Family/Group Info
    adults_count = db.Column(db.Integer, default=1)
    children_ages = db.Column(db.Text)  # JSON string of ages
    senior_travelers = db.Column(db.Boolean, default=False)
    
    # Preferences
    preferred_accommodation = db.Column(db.String(100))
    notification_preferences = db.Column(db.Text)  # JSON string
    
    # User preferences (JSON)
    preferences = db.Column(db.Text, default='{"email_notifications": true}')
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Relationships
    travel_briefs = db.relationship('TravelBrief', backref='user', lazy=True)
    travel_groups = db.relationship('TravelGroup', backref='owner', lazy=True, cascade='all, delete-orphan')
    schools = db.relationship('UserSchool', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convert user to dictionary"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone': self.phone,
            'home_airports': self.home_airports,
            'preferred_airlines': self.preferred_airlines,
            'dietary_restrictions': self.dietary_restrictions,
            'travel_style': self.travel_style,
            'adults_count': self.adults_count,
            'children_ages': self.children_ages,
            'senior_travelers': self.senior_travelers,
            'preferred_accommodation': self.preferred_accommodation,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class TravelBrief(db.Model):
    """Travel brief model for storing search criteria"""
    __tablename__ = 'travel_briefs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    departure_location = db.Column(db.String(100), nullable=False)
    destination = db.Column(db.String(100), nullable=False)
    departure_date = db.Column(db.DateTime, nullable=False)
    return_date = db.Column(db.DateTime, nullable=True)
    travelers = db.Column(db.String(100), nullable=False)
    budget_min = db.Column(db.Float, default=0)
    budget_max = db.Column(db.Float, default=0)
    accommodation_type = db.Column(db.String(50), nullable=False)
    interests = db.Column(db.Text)
    trip_length = db.Column(db.Float, default=5.0)
    priority = db.Column(db.String(20), default='medium')  # low, medium, high
    date_flexibility = db.Column(db.Integer, default=2)  # days of flexibility
    inspiration_sources = db.Column(db.Text)
    amadeus_destination_code = db.Column(db.String(10))
    
    # Tracking and Status
    status = db.Column(db.String(20), default='active')  # active, paused, completed, cancelled
    last_deal_check = db.Column(db.DateTime)
    deal_notifications = db.Column(db.Boolean, default=True)
    email_notifications = db.Column(db.Boolean, default=True)
    sms_notifications = db.Column(db.Boolean, default=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'departure_location': self.departure_location,
            'destination': self.destination,
            'departure_date': self.departure_date.isoformat() if self.departure_date else None,
            'return_date': self.return_date.isoformat() if self.return_date else None,
            'travelers': self.travelers,
            'budget_min': self.budget_min,
            'budget_max': self.budget_max,
            'accommodation_type': self.accommodation_type,
            'interests': self.interests,
            'trip_length': self.trip_length,
            'priority': self.priority,
            'date_flexibility': self.date_flexibility,
            'inspiration_sources': self.inspiration_sources,
            'amadeus_destination_code': self.amadeus_destination_code,
            'status': self.status,
            'last_deal_check': self.last_deal_check.isoformat() if self.last_deal_check else None,
            'deal_notifications': self.deal_notifications,
            'email_notifications': self.email_notifications,
            'sms_notifications': self.sms_notifications,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class Deal(db.Model):
    """Deal model for tracking matched travel deals"""
    __tablename__ = 'deals'
    
    id = db.Column(db.Integer, primary_key=True)
    brief_id = db.Column(db.Integer, db.ForeignKey('travel_briefs.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Deal Information
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    original_price = db.Column(db.Float)
    discount_percentage = db.Column(db.Float)
    provider = db.Column(db.String(100))
    booking_url = db.Column(db.Text)
    
    # Deal Specifics
    destination = db.Column(db.String(100), nullable=False)
    departure_location = db.Column(db.String(100), nullable=False)
    departure_date = db.Column(db.DateTime, nullable=False)
    return_date = db.Column(db.DateTime)
    accommodation_type = db.Column(db.String(50))
    
    # Additional Deal Fields for booking
    airline = db.Column(db.String(100))
    hotel_name = db.Column(db.String(200))
    hotel_rating = db.Column(db.Integer)
    total_price = db.Column(db.Float)
    currency = db.Column(db.String(10), default='GBP')
    type = db.Column(db.String(50), default='flight')  # flight, hotel, package
    
    # Deal Status
    status = db.Column(db.String(20), default='active')  # active, expired, booked, hidden
    match_score = db.Column(db.Float, default=0.0)  # How well it matches the brief
    notification_sent = db.Column(db.Boolean, default=False)
    expires_at = db.Column(db.DateTime)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    brief = db.relationship('TravelBrief', backref='deals', lazy=True)
    user = db.relationship('User', backref='deals', lazy=True)
    
    def to_dict(self):
        """Convert deal to dictionary"""
        return {
            'id': self.id,
            'brief_id': self.brief_id,
            'user_id': self.user_id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'original_price': self.original_price,
            'discount_percentage': self.discount_percentage,
            'provider': self.provider,
            'booking_url': self.booking_url,
            'destination': self.destination,
            'departure_location': self.departure_location,
            'departure_date': self.departure_date.isoformat() if self.departure_date else None,
            'return_date': self.return_date.isoformat() if self.return_date else None,
            'accommodation_type': self.accommodation_type,
            'airline': self.airline,
            'hotel_name': self.hotel_name,
            'hotel_rating': self.hotel_rating,
            'total_price': self.total_price or self.price,
            'currency': self.currency,
            'type': self.type,
            'status': self.status,
            'match_score': self.match_score,
            'notification_sent': self.notification_sent,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class Person(db.Model):
    """Reusable person profiles that can be added to multiple groups"""
    __tablename__ = 'people'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100))
    nickname = db.Column(db.String(50))  # For display purposes
    date_of_birth = db.Column(db.Date)
    person_type = db.Column(db.String(20), default='adult')  # adult, child, senior, infant
    
    # Additional info
    passport_number = db.Column(db.String(50))
    passport_expiry = db.Column(db.Date)
    dietary_restrictions = db.Column(db.Text)
    medical_notes = db.Column(db.Text)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='people', lazy=True)
    
    def to_dict(self):
        """Convert person to dictionary"""
        from datetime import date
        age = None
        if self.date_of_birth:
            today = date.today()
            age = today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        
        return {
            'id': self.id,
            'user_id': self.user_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'nickname': self.nickname,
            'full_name': f"{self.first_name} {self.last_name or ''}".strip(),
            'display_name': self.nickname or self.first_name,
            'date_of_birth': self.date_of_birth.isoformat() if self.date_of_birth else None,
            'age': age,
            'person_type': self.person_type,
            'passport_number': self.passport_number,
            'passport_expiry': self.passport_expiry.isoformat() if self.passport_expiry else None,
            'dietary_restrictions': self.dietary_restrictions,
            'medical_notes': self.medical_notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class GroupMember(db.Model):
    """Association table for people in groups"""
    __tablename__ = 'group_members'
    
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('travel_groups.id'), nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=False)
    role = db.Column(db.String(50))  # primary, spouse, child, friend, etc.
    
    # Relationships
    group = db.relationship('TravelGroup', backref='group_members', lazy=True)
    person = db.relationship('Person', backref='group_memberships', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'group_id': self.group_id,
            'person_id': self.person_id,
            'role': self.role,
            'person': self.person.to_dict() if self.person else None
        }


class TravelGroup(db.Model):
    """Travel group model for managing different travel configurations"""
    __tablename__ = 'travel_groups'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    group_name = db.Column(db.String(100), nullable=False)
    group_type = db.Column(db.String(50))  # individual, family, friends, custom
    is_primary = db.Column(db.Boolean, default=False)  # Mark as primary group
    
    # Group members stored as JSON (legacy - will migrate to GroupMember)
    members = db.Column(db.Text, nullable=False, default='[]')  # JSON array of {name, type, age, dob}
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert group to dictionary"""
        import json
        return {
            'id': self.id,
            'user_id': self.user_id,
            'group_name': self.group_name,
            'group_type': self.group_type,
            'members': json.loads(self.members) if self.members else [],
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class UserSchool(db.Model):
    """User school/council association for term dates"""
    __tablename__ = 'user_schools'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    school_key = db.Column(db.String(100), nullable=False)  # Key from UK_SCHOOLS_DATABASE
    school_name = db.Column(db.String(200), nullable=False)
    school_type = db.Column(db.String(50))  # 'council', 'independent', 'academy', etc.
    region = db.Column(db.String(100))
    country = db.Column(db.String(50))
    is_primary = db.Column(db.Boolean, default=False)  # Primary school for this user
    child_name = db.Column(db.String(100))  # Optional: which child attends this school
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'school_key': self.school_key,
            'school_name': self.school_name,
            'school_type': self.school_type,
            'region': self.region,
            'country': self.country,
            'is_primary': self.is_primary,
            'child_name': self.child_name,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


# Booking model removed - TravelAiGent is a deal finder that redirects to external booking partners