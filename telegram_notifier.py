import requests
import logging
from datetime import datetime
import config

class TelegramNotifier:
    def __init__(self):
        """Initialize Telegram notifier"""
        self.bot_token = config.TELEGRAM_BOT_TOKEN
        self.chat_id = config.TELEGRAM_CHAT_ID
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}"
    
    def send_alert(self, deal, analysis, brief):
        """Send travel deal alert via Telegram"""
        try:
            message = self.format_deal_message(deal, analysis, brief)
            
            payload = {
                'chat_id': self.chat_id,
                'text': message,
                'parse_mode': 'HTML',
                'disable_web_page_preview': False
            }
            
            response = requests.post(f"{self.base_url}/sendMessage", 
                                   json=payload, 
                                   timeout=30)
            
            if response.status_code == 200:
                logging.info(f"Telegram alert sent successfully for {deal.get('destination')}")
            else:
                logging.error(f"Failed to send Telegram alert: {response.text}")
                
        except Exception as e:
            logging.error(f"Error sending Telegram alert: {e}")
    
    def format_deal_message(self, deal, analysis, brief):
        """Format deal information into a Telegram message"""
        
        # Determine emoji based on score
        score = analysis.get('score', 0)
        if score >= 9:
            emoji = "🔥🔥🔥"
        elif score >= 8:
            emoji = "🔥🔥"
        else:
            emoji = "🔥"
        
        # Format price per person
        total_price = deal.get('total_price', 0)
        price_per_person = total_price / 4 if total_price else 0
        
        # Get brief information
        brief_id = brief.get('Brief_ID', 'Unknown')
        brief_name = brief.get('Brief_Name', 'Unknown Brief')
        
        # Format message
        message = f"""
{emoji} <b>TRAVEL DEAL ALERT</b> {emoji}

📋 <b>Brief:</b> {brief_id} - {brief_name}

<b>✈️ {deal.get('origin', 'N/A')} → {deal.get('destination', 'N/A')}</b>

📅 <b>Departure:</b> {deal.get('departure_date', 'N/A')} at {deal.get('departure_time', 'N/A')}
📅 <b>Return:</b> {deal.get('return_date', 'N/A')} at {deal.get('return_time', 'N/A')}

💰 <b>Total Price:</b> £{total_price:,.0f} ({deal.get('currency', 'GBP')})
💰 <b>Per Person:</b> £{price_per_person:,.0f}

🏢 <b>Airline:</b> {deal.get('airline', 'N/A')}
🔄 <b>Stops:</b> {deal.get('stops', 'N/A')}
⏱️ <b>Duration:</b> {deal.get('duration', 'N/A')}

<b>🤖 AI ANALYSIS</b>
📊 <b>Score:</b> {score}/10
🎯 <b>Recommendation:</b> {analysis.get('recommendation', 'N/A')}

💡 <b>Why it's good:</b>
{self.format_list(analysis.get('key_pros', []))}

⚠️ <b>Consider:</b>
{self.format_list(analysis.get('key_cons', []))}

📝 <b>Summary:</b> {analysis.get('action_summary', 'No summary available')}

💼 <b>Brief:</b> {brief.get('Brief_ID', 'N/A')} - {brief.get('Destinations', 'N/A')}

<i>Found by Travel AiGent at {datetime.now().strftime('%H:%M on %d/%m/%Y')}</i>
"""
        
        return message.strip()
    
    def format_list(self, items):
        """Format a list of items for Telegram message"""
        if not items:
            return "• Not specified"
        
        formatted_items = []
        for item in items[:3]:  # Limit to 3 items to keep message concise
            formatted_items.append(f"• {item}")
        
        return "\n".join(formatted_items)
    
    def send_status_update(self, message):
        """Send a general status update"""
        try:
            payload = {
                'chat_id': self.chat_id,
                'text': f"🤖 <b>Travel AiGent Status</b>\n\n{message}",
                'parse_mode': 'HTML'
            }
            
            response = requests.post(f"{self.base_url}/sendMessage", 
                                   json=payload, 
                                   timeout=30)
            
            if response.status_code == 200:
                logging.info("Status update sent via Telegram")
            else:
                logging.error(f"Failed to send status update: {response.text}")
                
        except Exception as e:
            logging.error(f"Error sending status update: {e}")
    
    def test_connection(self):
        """Test Telegram bot connection"""
        try:
            response = requests.get(f"{self.base_url}/getMe", timeout=30)
            
            if response.status_code == 200:
                bot_info = response.json()
                logging.info(f"Telegram bot connected: {bot_info['result']['first_name']}")
                return True
            else:
                logging.error(f"Telegram bot test failed: {response.text}")
                return False
                
        except Exception as e:
            logging.error(f"Error testing Telegram connection: {e}")
            return False
