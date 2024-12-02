import logging


def get_logger(name: str) -> logging.Logger:
    """
    Creates and returns a logger with the specified name. If the logger does not
    already have handlers, it adds a StreamHandler with a specific formatter and
    sets the logging level to DEBUG.

    Args:
        name (str): The name of the logger.

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)
    if not logger.hasHandlers():
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
    return logger
