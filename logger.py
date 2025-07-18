import logging
import sys
from datetime import datetime
import config

def setup_logging():
    """Set up comprehensive logging for the Travel AiGent system"""
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Get log level from config
    log_level = getattr(logging, config.LOG_LEVEL.upper(), logging.INFO)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # Remove existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # File handler for persistent logging
    try:
        file_handler = logging.FileHandler('travel_agent.log')
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
    except Exception as e:
        # If file logging fails, just use console
        logging.warning(f"Could not set up file logging: {e}")
    
    # Set specific loggers to appropriate levels
    logging.getLogger('requests').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('gspread').setLevel(logging.WARNING)
    
    # Log startup message
    logging.info("="*50)
    logging.info("Travel AiGent Logging System Initialized")
    logging.info(f"Log Level: {config.LOG_LEVEL}")
    logging.info(f"Timestamp: {datetime.now().isoformat()}")
    logging.info("="*50)

def get_logger(name):
    """Get a logger instance for a specific module"""
    return logging.getLogger(name)
