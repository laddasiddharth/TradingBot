import logging
import logging.handlers
import os

def setup_logging(log_filename="trading_bot.log"):
    """Configures application-wide logging."""
    logger = logging.getLogger("trading_bot")
    logger.setLevel(logging.DEBUG)

    # Prevent adding handlers multiple times
    if logger.hasHandlers():
        return logger

    # Log formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # File handler
    file_handler = logging.handlers.RotatingFileHandler(
        log_filename, maxBytes=5*1024*1024, backupCount=2
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
