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

def storage_handler(event):

    # file_path = DATA_PATH / f"traffic_{datetime.now().strftime('%Y-%m-%d')}.jsonl"

    # with open(file_path, "a") as f:
    #     f.write(json.dumps(event) + "\n")
    db_client.insert_event(event)
    # db_client.compute_metrics()
    logger.info(f"Stored event for {event.get('road_name')}")


if __name__ == "__main__":
    consumer = KafkaConsumerClient(
        handler=storage_handler,
        group_id="storage_group"
    )
    consumer.start()
