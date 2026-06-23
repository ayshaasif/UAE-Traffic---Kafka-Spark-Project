from collections import defaultdict, deque

from streaming.consumer import KafkaConsumerClient
from utils.logger import get_logger
import smtplib
from email.mime.text import MIMEText


logger = get_logger("analytics_consumer")
import json
from datetime import datetime
from pathlib import Path
from streaming.consumer import KafkaConsumerClient
from storage.postgres_client import PostgresClient
from utils.logger import get_logger

logger = get_logger("storage_consumer")

DATA_PATH = Path("data/raw")
DATA_PATH.mkdir(parents=True, exist_ok=True)
db_client = PostgresClient()


# simple rolling window in memory
road_speed_window = defaultdict(lambda: deque(maxlen=10))


def analytics_handler(event):

    road = event.get("road_name")
    speed = event.get("current_speed")

    if road and speed is not None:

        road_speed_window[road].append(speed)

        avg_speed = sum(road_speed_window[road]) / len(road_speed_window[road])

        logger.info(
            f"[ANALYTICS] {road} | "
            f"avg_speed={avg_speed:.2f} | "
            f"latest={speed}"
        )

        if avg_speed < 30:
            logger.warning(
                f"🚨 ANALYTICS ALERT: {road} average speed is low at {avg_speed:.2f} km/h"
            )


if __name__ == "__main__":
    consumer = KafkaConsumerClient(
        handler=analytics_handler,
        group_id="analytics_group"
    )
    consumer.start()
