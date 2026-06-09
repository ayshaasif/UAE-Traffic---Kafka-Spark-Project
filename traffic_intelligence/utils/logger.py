import logging
import os
from datetime import datetime

os.makedirs("logs", exist_ok=True)

def get_logger(name="traffic_pipeline"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s"
        )

        # File log
        file_handler = logging.FileHandler(
            f"logs/pipeline_{datetime.now().strftime('%Y-%m-%d')}.log"
        )
        file_handler.setFormatter(formatter)

        # Console log
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger
