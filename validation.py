"""Input validation schemas for Travel AiGent."""
from marshmallow import Schema, fields, validate, ValidationError
import re


class BriefSchema(Schema):
    """Validation schema for travel brief data."""
    
    brief_name = fields.Str(
        required=True, 
        validate=validate.Length(min=1, max=200),
        error_messages={'required': 'Brief name is required.'}
    )
    
    priority = fields.Str(
        required=True,
        validate=validate.OneOf(['Low', 'Medium', 'High']),
        error_messages={'required': 'Priority is required.'}
    )
    
    departure_location = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=100),
        error_messages={'required': 'Departure location is required.'}
    )
    
    destinations = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=500),
        error_messages={'required': 'Destinations are required.'}
    )
    
    travel_dates = fields.Str(
        required=False,
        validate=validate.Length(min=1, max=100),
        allow_none=True
    )
    
    departure_date = fields.Date(
        required=False,
        allow_none=True
    )
    
    return_date = fields.Date(
        required=False,
        allow_none=True
    )
    
    date_flexibility = fields.Int(
        validate=validate.Range(min=0, max=7),
        load_default=2
    )
    
    trip_duration = fields.Str(
        required=False,
        validate=validate.OneOf(['3-4 nights', '5-7 nights', '7-10 nights', '10+ nights']),
        allow_none=True
    )
    
    search_type = fields.Str(
        required=False,
        validate=validate.OneOf(['flight_only', 'hotel_only', 'flight_and_hotel']),
        load_default='flight_and_hotel'
    )
    
    travelers = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=100),
        error_messages={'required': 'Travelers information is required.'}
    )
    
    budget_min = fields.Int(
        validate=validate.Range(min=0, max=50000),
        load_default=0,
        error_messages={'invalid': 'Budget must be a valid number.'}
    )
    
    budget_max = fields.Int(
        validate=validate.Range(min=0, max=100000),
        load_default=0,
        error_messages={'invalid': 'Budget must be a valid number.'}
    )
    
    accommodation_type = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=500),
        error_messages={'required': 'Accommodation type is required.'}
    )
    
    flight_class = fields.Str(
        required=True,
        validate=validate.OneOf([
            'Economy', 
            'Economy with comfort', 
            'Premium Economy', 
            'Business'
        ]),
        error_messages={'required': 'Flight class is required.'}
    )
    
    ai_instructions = fields.Str(
        validate=validate.Length(max=1000),
        load_default='',
        allow_none=True
    )


class QueryParamsSchema(Schema):
    """Validation schema for API query parameters."""
    
    min_score = fields.Float(
        validate=validate.Range(min=0, max=10),
        load_default=5.0
    )
    
    max_price = fields.Float(
        validate=validate.Range(min=0),
        load_default=999999
    )
    
    destination = fields.Str(
        validate=validate.Length(max=100),
        load_default=''
    )
    
    limit = fields.Int(
        validate=validate.Range(min=1, max=50),
        load_default=10
    )


def validate_brief_id(brief_id: str) -> bool:
    """Validate brief ID format."""
    # Allow alphanumeric, hyphens, and underscores, max 50 chars
    pattern = r'^[a-zA-Z0-9_-]{1,50}$'
    return bool(re.match(pattern, brief_id))


def sanitize_string(value: str) -> str:
    """Basic string sanitization."""
    if not isinstance(value, str):
        return str(value)
    
    # Remove potentially dangerous characters
    # Keep alphanumeric, spaces, and basic punctuation
    import html
    sanitized = html.escape(value.strip())
    
    # Limit length
    return sanitized[:1000]


def validate_and_sanitize_brief(data: dict) -> dict:
    """Validate and sanitize brief data."""
    schema = BriefSchema()
    
    try:
        # Validate data structure
        validated_data = schema.load(data)
        
        # Additional sanitization
        for key, value in validated_data.items():
            if isinstance(value, str):
                validated_data[key] = sanitize_string(value)
        
        return validated_data
        
    except ValidationError as err:
        raise ValueError(f"Validation error: {err.messages}")


def validate_query_params(params: dict) -> dict:
    """Validate API query parameters."""
    schema = QueryParamsSchema()
    
    try:
        return schema.load(params)
    except ValidationError as err:
        raise ValueError(f"Invalid query parameters: {err.messages}")