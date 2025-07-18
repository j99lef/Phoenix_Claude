import gspread
import logging
import json
from datetime import datetime, timedelta
from oauth2client.service_account import ServiceAccountCredentials
import config
import pandas as pd

class SheetsHandler:
    def __init__(self):
        """Initialize Google Sheets handler"""
        self.client = None
        self.sheet = None
        self.connect_to_sheets()
    
    def connect_to_sheets(self):
        """Connect to Google Sheets using service account credentials"""
        try:
            # Use JSON credentials from environment variable
            if config.GOOGLE_CREDENTIALS_JSON:
                import json
                creds_dict = json.loads(config.GOOGLE_CREDENTIALS_JSON)
                scope = ['https://spreadsheets.google.com/feeds',
                        'https://www.googleapis.com/auth/drive']
                
                creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
                self.client = gspread.authorize(creds)
                self.sheet = self.client.open_by_key(config.GOOGLE_SHEET_ID)
                
                logging.info("Successfully connected to Google Sheets")
            else:
                logging.error("Google Sheets credentials not found in environment variables")
                
        except Exception as e:
            logging.error(f"Failed to connect to Google Sheets: {e}")
            # Create mock client for development/testing
            self.client = None
            self.sheet = None
    
    def get_active_briefs(self):
        """Get all active travel briefs from the sheet"""
        try:
            if not self.sheet:
                # Return mock data for development
                return self._get_mock_briefs()
            
            # Get the 'ACTIVE TRAVEL BRIEFS' worksheet
            worksheet = self.sheet.worksheet('ACTIVE TRAVEL BRIEFS')
            
            # Get all records
            records = worksheet.get_all_records()
            
            # Filter for active briefs
            active_briefs = []
            for record in records:
                if record.get('Status', '').lower() == 'active':
                    active_briefs.append(record)
            
            logging.info(f"Retrieved {len(active_briefs)} active travel briefs")
            return active_briefs
            
        except Exception as e:
            logging.error(f"Error getting active briefs: {e}")
            return self._get_mock_briefs()
    
    def _get_mock_briefs(self):
        """Return mock travel briefs for development/testing"""
        return [
            {
                'Brief_ID': 'MOCK_001',
                'Status': 'active',
                'Destinations': 'Paris, Rome',
                'Budget_Max': '1500',
                'Travel_Dates': '2025-08-15 - 2025-08-22',
                'Trip_Duration': '7 days',
                'Travelers': '4 people',
                'Departure_Location': 'London',
                'AI_Instructions': 'Looking for family-friendly destinations with cultural activities',
                'Notes': 'Summer holiday for family with teenagers',
                'Created_Date': '2025-06-01',
                'Last_Checked': ''
            }
        ]
    
    def log_deal(self, deal, analysis, brief):
        """Log a deal and its analysis to the sheet"""
        try:
            if not self.sheet:
                logging.info(f"Mock: Would log deal to sheet - {deal.get('destination')} - Score: {analysis.get('score')}")
                return
            
            # Get or create the 'DEAL HISTORY (HEADERS)' worksheet
            try:
                worksheet = self.sheet.worksheet('DEAL HISTORY (HEADERS)')
            except gspread.WorksheetNotFound:
                # Create the worksheet if it doesn't exist
                worksheet = self.sheet.add_worksheet(title='DEAL HISTORY (HEADERS)', rows=1000, cols=20)
                # Add headers
                headers = [
                    'Timestamp', 'Brief_ID', 'Deal_Type', 'Origin', 'Destination',
                    'Departure_Date', 'Return_Date', 'Total_Price', 'Currency',
                    'Airline', 'AI_Score', 'Recommendation', 'Value_Assessment',
                    'Family_Suitability', 'Key_Pros', 'Key_Cons', 'Action_Summary'
                ]
                worksheet.append_row(headers)
            
            # Prepare row data
            row_data = [
                datetime.now().isoformat(),
                brief.get('Brief_ID', ''),
                deal.get('type', ''),
                deal.get('origin', ''),
                deal.get('destination', ''),
                deal.get('departure_date', ''),
                deal.get('return_date', ''),
                deal.get('total_price', ''),
                deal.get('currency', ''),
                deal.get('airline', ''),
                analysis.get('score', ''),
                analysis.get('recommendation', ''),
                analysis.get('value_assessment', ''),
                analysis.get('family_suitability', ''),
                '; '.join(analysis.get('key_pros', [])),
                '; '.join(analysis.get('key_cons', [])),
                analysis.get('action_summary', '')
            ]
            
            worksheet.append_row(row_data)
            logging.info(f"Deal logged to Google Sheets: {deal.get('destination')} - Score: {analysis.get('score')}")
            
        except Exception as e:
            logging.error(f"Error logging deal to sheet: {e}")
    
    def update_brief_timestamp(self, brief_id):
        """Update the last checked timestamp for a brief"""
        try:
            if not self.sheet:
                logging.info(f"Mock: Would update timestamp for brief {brief_id}")
                return
            
            worksheet = self.sheet.worksheet('ACTIVE TRAVEL BRIEFS')
            
            # Find the row with the matching Brief_ID
            cell = worksheet.find(brief_id)
            if cell:
                # Update the Last_Checked column (assuming it's column with header 'Last_Checked')
                headers = worksheet.row_values(1)
                if 'Last_Checked' in headers:
                    col_index = headers.index('Last_Checked') + 1
                    worksheet.update_cell(cell.row, col_index, datetime.now().isoformat())
                    logging.info(f"Updated timestamp for brief {brief_id}")
            
        except Exception as e:
            logging.error(f"Error updating brief timestamp: {e}")
    
    def is_duplicate_deal(self, deal):
        """Check if this deal has been logged recently to avoid duplicates"""
        try:
            if not self.sheet:
                # For mock, assume no duplicates
                return False
            
            worksheet = self.sheet.worksheet('DEAL HISTORY (HEADERS)')
            
            # Get recent deals (last 24 hours)
            recent_cutoff = (datetime.now() - timedelta(hours=24)).isoformat()
            
            # Simple check - in production you might want more sophisticated logic
            records = worksheet.get_all_records()
            
            for record in records:
                if (record.get('Destination') == deal.get('destination') and
                    record.get('Departure_Date') == deal.get('departure_date') and
                    record.get('Total_Price') == deal.get('total_price') and
                    record.get('Timestamp', '') > recent_cutoff):
                    
                    logging.info(f"Duplicate deal detected: {deal.get('destination')} on {deal.get('departure_date')}")
                    return True
            
            return False
            
        except Exception as e:
            logging.error(f"Error checking for duplicate deal: {e}")
            return False
    
    def get_recent_deals(self, limit=20):
        """Get recent deals for the web interface"""
        try:
            if not self.sheet:
                # Return mock data
                return [
                    {
                        'timestamp': '2025-06-27T10:30:00',
                        'destination': 'Paris',
                        'price': '£450',
                        'score': 8,
                        'recommendation': 'BOOK_NOW'
                    },
                    {
                        'timestamp': '2025-06-27T10:25:00',
                        'destination': 'Rome',
                        'price': '£520',
                        'score': 7,
                        'recommendation': 'WATCH'
                    }
                ]
            
            worksheet = self.sheet.worksheet('DEAL HISTORY (HEADERS)')
            records = worksheet.get_all_records()
            
            # Sort by timestamp and get latest
            sorted_records = sorted(records, 
                                  key=lambda x: x.get('Timestamp', ''), 
                                  reverse=True)
            
            return sorted_records[:limit]
            
        except Exception as e:
            logging.error(f"Error getting recent deals: {e}")
            return []
