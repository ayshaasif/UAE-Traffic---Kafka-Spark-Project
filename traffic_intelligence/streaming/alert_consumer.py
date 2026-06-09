from streaming.consumer import KafkaConsumerClient
from utils.logger import get_logger
import mailtrap as mt
import os

from dotenv import load_dotenv
load_dotenv()

logger = get_logger("alert_consumer")

CONGESTION_THRESHOLD = 0.5



def send_mail_trap_alert(road, congestion):

    mail = mt.Mail(
        sender=mt.Address(email="hello@demomailtrap.co", name="Mailtrap Test"),
        to=[mt.Address(email="ayshaasif14@gmail.com")],
        subject="Traffic Congestion Alert!",
        text=f"Alert: {road} is experiencing heavy congestion with a congestion index of {congestion}.",
        category="Integration Test",
    )

    client = mt.MailtrapClient(token=os.getenv("MAIL_TRAP_API_KEY"))
    response = client.send(mail)

    print(f"Response: {response}")

def alert_handler(event):

    road = event.get("road_name")
    congestion = event.get("congestion_index", 0)

    if congestion >= CONGESTION_THRESHOLD:
        send_mail_trap_alert(road, congestion)

        logger.warning(
            f"🚨 TRAFFIC ALERT: {road} "
            f"congestion={congestion}"
        )


if __name__ == "__main__":
    consumer = KafkaConsumerClient(
        handler=alert_handler,
        group_id="alert_group"
    )
    consumer.start()

