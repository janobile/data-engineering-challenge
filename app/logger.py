import logging

def setup_logger(level=logging.INFO):
    # Create a logger instance
    logger = logging.getLogger(__name__)
    # Set the logging level (you can adjust as needed)
    logger.setLevel(level)

    # Add the stream handler to the logger
    if not logger.handlers:
        # Create a formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # Create a stream handler
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

    return logger
