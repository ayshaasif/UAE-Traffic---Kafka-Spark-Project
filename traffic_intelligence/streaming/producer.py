import json

from confluent_kafka import Producer

from utils.logger import get_logger


logger = get_logger("kafka_producer")


class KafkaProducerClient:

    def __init__(self, bootstrap_servers="localhost:9092"):

        self.producer = Producer(
            {
                "bootstrap.servers": bootstrap_servers,
                "client.id": "traffic_producer",
                "acks": "all"
            }
        )

    def delivery_report(self, err, msg):

        if err is not None:
            logger.error(
                f"Delivery failed: {err}"
            )
        else:
            logger.info(
                f"Delivered topic={msg.topic()} "
                f"partition={msg.partition()} "
                f"offset={msg.offset()}"
            )

    def send_message(self, topic, data):

        try:

            self.producer.produce(
                topic=topic,
                key=str(data.get("road_id", "unknown")),
                value=json.dumps(data).encode("utf-8"),
                callback=self.delivery_report
            )

            self.producer.poll(0)

        except Exception:
            logger.exception(
                "Failed to send Kafka message"
            )

    def flush(self):
        self.producer.flush()
        