#!/usr/bin/env python3
"""
Start the web server with background scheduler
This allows Railway to run both web and scheduler in a single process
"""
import os
import sys
import threading
import time
import logging
import schedule

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from travel_agent import TravelAgent
from app import app

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def run_scheduler():
    """Run the scheduler in a background thread"""
    logging.info("Starting background scheduler thread...")
    
    try:
        agent = TravelAgent()
        
        # Schedule regular searches every 6 hours as requested
        schedule.every(6).hours.do(agent.run_deal_search)
        
        # Run an initial check after 2 minutes to catch any new briefs
        def initial_check():
            logging.info("Running initial search check...")
            agent.run_deal_search()
            # Clear this one-time job
            return schedule.CancelJob
        
        schedule.every(2).minutes.do(initial_check)
        
        logging.info("Scheduler configured - will check every 6 hours")
        
        while True:
            try:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
            except Exception as e:
                logging.error(f"Scheduler error: {e}", exc_info=True)
                time.sleep(300)  # Wait 5 minutes on error
                
    except Exception as e:
        logging.error(f"Failed to start scheduler: {e}", exc_info=True)

if __name__ == "__main__":
    # Start scheduler in background thread
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()
    logging.info("Background scheduler thread started")
    
    # Run the Flask app
    port = int(os.environ.get("PORT", 5000))
    logging.info(f"Starting web server on port {port}")
    
    # Use production server if available
    try:
        from gunicorn.app.base import BaseApplication
        
        class StandaloneApplication(BaseApplication):
            def __init__(self, app, options=None):
                self.options = options or {}
                self.application = app
                super().__init__()
            
            def load_config(self):
                for key, value in self.options.items():
                    self.cfg.set(key.lower(), value)
            
            def load(self):
                return self.application
        
        options = {
            'bind': f'0.0.0.0:{port}',
            'workers': 1,  # Single worker to ensure scheduler runs
            'threads': 2,
            'accesslog': '-',
            'errorlog': '-',
            'log_level': 'info',
            'preload_app': True
        }
        
        StandaloneApplication(app, options).run()
        
    except ImportError:
        # Fallback to development server
        logging.warning("Gunicorn not available, using development server")
        app.run(host="0.0.0.0", port=port, debug=False)