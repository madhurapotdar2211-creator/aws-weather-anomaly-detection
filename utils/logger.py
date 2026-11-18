import logging
from config.config import LOG_PATH

def get_logger(name="weather-monitoring"):
    """Return a consistent file and console logger."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
        handler = logging.FileHandler(LOG_PATH / "application.log", encoding="utf-8")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger
