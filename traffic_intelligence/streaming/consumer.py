import json
import uuid
from utils.logger import get_logger

from confluent_kafka import Consumer, KafkaError

logger = get_logger(__name__)

class KafkaConsumerClient:
    def __init__(self, bootstrap_servers="localhost:19092", group_id="traffic_consumer_group", topic="traffic.raw", handler=None):
        self.consumer = Consumer({
            "bootstrap.servers": bootstrap_servers,
            "group.id": group_id,
            "auto.offset.reset": "earliest",
            "enable.auto.commit": True
        })
        self.topic = topic
        self.consumer.subscribe([self.topic])
        self.handler = handler

    def start(self):
        logger.info(f"Starting Kafka consumer for topic '{self.topic}'... ")

        try:
            while True:
                msg = self.consumer.poll(1.0) # Poll for messages with a timeout of 1 second

                if msg is None:
                    continue # No message received, continue polling
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        logger.info(f"[INFO] End of partition reached {msg.topic()} [{msg.partition()}]")
                    else:
                        logger.info(f"[ERROR] Kafka error: {msg.error()}")
                    continue

                # Process the received message
                try:
                    event = json.loads(msg.value().decode('utf-8'))
                    self.handler(event) if self.handler else None
                    logger.info(f"[INFO] Received message")
                except json.JSONDecodeError as e:
                    logger.info(f"[ERROR] Failed to decode JSON: {e}")
        except KeyboardInterrupt:
            logger.info("[INFO] Consumer interrupted by user, shutting down...")
        finally:
            self.consumer.close()




# if __name__ == "__main__":
#     consumer = KafkaConsumerClient()
#     consumer.start()
