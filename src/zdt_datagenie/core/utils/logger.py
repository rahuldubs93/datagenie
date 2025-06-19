import logging
import os


def get_logger(name: str):
    log_level = os.getenv("LOG_LEVEL", "ERROR").upper()
    log_level = getattr(logging, log_level, logging.ERROR)
    if len(logging.getLogger().handlers) > 0:
        logger = logging.getLogger(name)
        logger.setLevel(log_level)
        return logger
    else:
        logging.basicConfig(level=log_level)
        return logging
