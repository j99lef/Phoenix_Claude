import json
import logging
import time
from datetime import datetime
import config
from openai import OpenAI

class OpenAIAnalyzer:
    def __init__(self):
        """Initialize OpenAI analyzer"""
        self.client = OpenAI(api_key=config.OPENAI_API_KEY)
        self.last_request_time = 0
    
    def rate_limit(self):
        """Implement rate limiting for OpenAI requests"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        min_interval = 60.0 / config.OPENAI_REQUESTS_PER_MINUTE
        
        if time_since_last < min_interval:
            sleep_time = min_interval - time_since_last
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()
    
    def analyze_deal(self, deal, brief):
        """Analyze deal suitability using OpenAI"""
        
        try:
            self.rate_limit()
            
            family_context = self.build_family_context(brief)
            deal_context = self.build_deal_context(deal)
            
            prompt = f"""
Analyze this travel deal for the Lefley family and provide a detailed assessment.

{family_context}

Travel Brief Context:
- Brief ID: {brief.get('Brief_ID', 'N/A')}
- Preferred destinations: {brief.get('Destinations', 'N/A')}
- Budget limit: £{brief.get('Budget_Max', 'N/A')}
- Travel dates: {brief.get('Travel_Dates', 'N/A')}
- Trip duration: {brief.get('Trip_Duration', 'N/A')}
- Travelers: {brief.get('Travelers', 'N/A')}
- Special requirements: {brief.get('AI_Instructions', 'None specified')}
- Additional notes: {brief.get('Notes', 'None')}

Deal Details:
{deal_context}

Please rate this deal from 1-10 considering:
1. Value for money compared to typical prices for this route
2. Family suitability (considering children ages 13 and 10)
3. Alignment with stated preferences and requirements
4. Practical considerations (flight times, connections, total travel time)
5. Seasonal timing and destination appeal
6. Budget alignment

Respond ONLY with valid JSON in this exact format:
{{
    "score": <number_1_to_10>,
    "recommendation": "<BOOK_NOW|WATCH|IGNORE>", 
    "value_assessment": "<brief explanation of value>",
    "family_suitability": "<brief explanation of family fit>",
    "key_pros": ["<pro1>", "<pro2>", "<pro3>"],
    "key_cons": ["<con1>", "<con2>"],
    "action_summary": "<one sentence recommendation>"
}}
"""
            
            # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
            # do not change this unless explicitly requested by the user
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
                temperature=0.3,
                max_tokens=800
            )
            
            analysis = self.parse_ai_response(response.choices[0].message.content)
            
            # Validate and sanitize the response
            analysis = self.validate_analysis(analysis)
            
            logging.info(f"AI analysis completed for {deal.get('destination', 'Unknown')} - Score: {analysis.get('score', 0)}")
            
            return analysis
            
        except Exception as e:
            logging.error(f"Error in AI analysis: {e}")
            # Return a default low-score analysis on error
            return {
                'score': 1,
                'recommendation': 'IGNORE',
                'value_assessment': 'Analysis failed',
                'family_suitability': 'Unable to assess',
                'key_pros': ['Analysis unavailable'],
                'key_cons': ['Technical error occurred'],
                'action_summary': 'Deal analysis failed - manual review required'
            }
    
    def build_family_context(self, brief):
        """Build comprehensive family context for AI analysis"""
        travelers = self.parse_travelers(brief.get('Travelers', ''))
        
        context = f"""
Family Profile: The Lefley Family from Wimbledon Park, London
- Parents: Jonathan (53) and Belinda (46) - experienced travelers
- Children: Martha (13) and Margot (10) - both always travel with family
- Optional: Tabitha (17) - rarely joins family holidays
- Current trip configuration: {travelers['total']} people total

Travel Preferences:
- Home airports: Heathrow (preferred), Gatwick, Stansted
- Previous successful trips: Dubai (loved), Rome city break (enjoyed)
- School constraints: Must work around Ricards Lodge High School holidays
- Family priorities: Educational value, reasonable travel times, child-friendly activities

Practical Considerations:
- Budget-conscious but willing to pay for quality family experiences
- Prefer direct flights or minimal connections when traveling with children
- Need family-friendly accommodations and activities
- Consider meal times and children's schedules
- Value destinations with mix of culture, history, and fun activities
"""
        return context
    
    def build_deal_context(self, deal):
        """Build detailed deal context for analysis"""
        context = f"""
Flight Deal Details:
- Route: {deal.get('origin', 'N/A')} → {deal.get('destination', 'N/A')}
- Departure: {deal.get('departure_date', 'N/A')} at {deal.get('departure_time', 'N/A')}
- Return: {deal.get('return_date', 'N/A')} at {deal.get('return_time', 'N/A')}
- Total price: £{deal.get('total_price', 'N/A')} {deal.get('currency', '')}
- Airline: {deal.get('airline', 'N/A')}
- Stops: {deal.get('stops', 'N/A')}
- Flight duration: {deal.get('duration', 'N/A')}
- Booking class: {deal.get('booking_class', 'N/A')}
- Seats available: {deal.get('seats_available', 'N/A')}
- Price per person: £{deal.get('total_price', 0) / 4 if deal.get('total_price') else 'N/A'}
"""
        return context
    
    def parse_ai_response(self, response_content):
        """Parse and validate AI response"""
        try:
            analysis = json.loads(response_content)
            return analysis
        except json.JSONDecodeError as e:
            logging.error(f"Failed to parse AI response as JSON: {e}")
            logging.error(f"Response content: {response_content}")
            # Try to extract JSON from response if it's wrapped in other text
            try:
                start = response_content.find('{')
                end = response_content.rfind('}') + 1
                if start >= 0 and end > start:
                    json_str = response_content[start:end]
                    return json.loads(json_str)
            except:
                pass
            
            # Return default structure on parse failure
            return {
                'score': 1,
                'recommendation': 'IGNORE',
                'value_assessment': 'Parse error',
                'family_suitability': 'Unknown',
                'key_pros': ['Unable to analyze'],
                'key_cons': ['Response parse failed'],
                'action_summary': 'Analysis failed - manual review needed'
            }
    
    def validate_analysis(self, analysis):
        """Validate and sanitize analysis results"""
        # Ensure required fields exist with defaults
        validated = {
            'score': max(1, min(10, int(analysis.get('score', 1)))),
            'recommendation': analysis.get('recommendation', 'IGNORE'),
            'value_assessment': str(analysis.get('value_assessment', 'Not assessed'))[:200],
            'family_suitability': str(analysis.get('family_suitability', 'Not assessed'))[:200],
            'key_pros': analysis.get('key_pros', ['Not specified'])[:5],  # Max 5 pros
            'key_cons': analysis.get('key_cons', ['Not specified'])[:5],  # Max 5 cons
            'action_summary': str(analysis.get('action_summary', 'No recommendation'))[:300]
        }
        
        # Validate recommendation values
        valid_recommendations = ['BOOK_NOW', 'WATCH', 'IGNORE']
        if validated['recommendation'] not in valid_recommendations:
            validated['recommendation'] = 'IGNORE'
        
        # Ensure lists are actually lists
        if not isinstance(validated['key_pros'], list):
            validated['key_pros'] = ['Not specified']
        if not isinstance(validated['key_cons'], list):
            validated['key_cons'] = ['Not specified']
        
        return validated
    
    def parse_travelers(self, travelers_str):
        """Parse travelers string - reuse from amadeus_api"""
        try:
            result = {'adults': 2, 'children': 2, 'total': 4}
            
            if not travelers_str:
                return result
            
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
                        result = {'adults': 2, 'children': 3, 'total': 5}
                    else:
                        result['total'] = total
            
            result['total'] = result['adults'] + result['children']
            return result
            
        except Exception as e:
            logging.error(f"Error parsing travelers '{travelers_str}': {e}")
            return {'adults': 2, 'children': 2, 'total': 4}
