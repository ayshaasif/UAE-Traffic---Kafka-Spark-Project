from ingestion.tomtom_client import get_raw_traffic
from ingestion.transformer import transform_traffic
from streaming.producer import KafkaProducerClient
from utils.logger import get_logger

from datetime import datetime
import time
import yaml
from pathlib import Path

logger = get_logger("traffic_collector")


BASE_DIR = Path(__file__).resolve().parent.parent


def load_roads():
    with open(BASE_DIR / "config" / "road_segments.yaml", "r") as file:
        return yaml.safe_load(file)["roads"]


def run():
    roads = load_roads()
    producer = KafkaProducerClient("localhost:19092")

    try:
        while True:
            for road in roads:

                try:
                    logger.info(
                        f"Processing {road['name']} "
                        f"({road['lat']}, {road['lon']})"
                    )

                    raw = get_raw_traffic(road["lat"], road["lon"])
                    event = transform_traffic(raw, road)

                    if event:
                        producer.send_message("traffic.raw", event)

                        logger.info(
                            f"{event['road_name']} congestion={event['congestion_index']}"
                        )

                except Exception:
                    logger.exception(
                        f"Failed processing road {road['name']}"
                    )

            logger.info("Cycle complete. Sleeping 300s")
            time.sleep(300)

    finally:
        logger.info("Flushing Kafka producer...")
        producer.flush()


if __name__ == "__main__":
    run()

    