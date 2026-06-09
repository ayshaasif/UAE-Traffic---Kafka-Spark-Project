import json
import os
import psycopg2
from dotenv import load_dotenv
load_dotenv()

from utils.logger import get_logger

logger = get_logger("postgres")

class PostgresClient:

    def __init__(self):

        self.conn = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT"),
            database=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD")
        )

        self.conn.autocommit = True

    def insert_event(self, event):

        query = """
        INSERT INTO traffic_events (
            road_id,
            road_name,
            current_speed,
            free_flow_speed,
            congestion_index,
            event_time,
            raw_event
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s)
        """

        with self.conn.cursor() as cur:

            cur.execute(
                query,
                (
                    event["road_id"],
                    event["road_name"],
                    event["current_speed"],
                    event["free_flow_speed"],
                    event["congestion_index"],
                    event["event_time"],
                    json.dumps(event)
                )
            )

        logger.info(
            f"Inserted road={event['road_name']}"
        )

        