import logging
import settings

def get_logger():
    logger = logging.getLogger('log_ship')
    logger.setLevel(settings.LOG_LEVEL)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    if settings.SELF_LOG_TO_CONSOLE:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    if settings.SELF_LOG_FILE_PATH:
        file_handler = logging.FileHandler(settings.SELF_LOG_FILE_PATH)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
