import logging
import logging.handlers


def get_logger(thread_name, file_name):
    # Create a custom logger
    logger = logging.getLogger(thread_name)

    # Set level of logger
    logger.setLevel(logging.DEBUG)

    central_handler = logging.handlers.RotatingFileHandler(file_name, maxBytes=10240000, encoding="UTF-8", backupCount=10)    # nopep8

    # Create a formatter
    formatter = logging.Formatter('%(asctime)s | %(name)s |  %(thread)-6s - %(levelname)-8s - %(filename)-10s:%(lineno)d - %(message)s', "%d.%m.%Y - %H:%M:%S")   # nopep8

    # Set formatter for each handler
    central_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(central_handler)

    return logger
