import logging

def logging_basic_config() -> logging.Logger:
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    return logger