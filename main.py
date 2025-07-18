import schedule
import time
import logging
import threading
from travel_agent import TravelAgent
from logger import setup_logging

def main():
    """Main entry point for the travel agent scheduler"""
    setup_logging()
    logging.info("Starting Travel AiGent system...")
    
    agent = TravelAgent()
    
    # Schedule checks every 6 hours between 9 AM and 9 PM
    schedule.every(6).hours.do(agent.run_deal_search)
    
    # Run an initial check after startup (delayed by 1 minute to allow web server to start)
    schedule.every(1).minutes.do(agent.run_initial_check).tag('initial')
    
    logging.info("Scheduler configured - checking every 6 hours")
    
    # Keep scheduler running
    while True:
        try:
            schedule.run_pending()
            time.sleep(60)  # Check every minute for scheduled tasks
        except KeyboardInterrupt:
            logging.info("Shutting down Travel AiGent...")
            break
        except Exception as e:
            logging.error(f"Scheduler error: {e}")
            time.sleep(300)  # Wait 5 minutes before retrying

if __name__ == "__main__":
    main()
