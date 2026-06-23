import time
from storage.postgres_client import PostgresClient

INTERVAL_SECONDS = 900  # 15 minutes

db_client = PostgresClient()

if __name__ == "__main__":
    print("[INFO] Metrics scheduler started...")

    while True:
        try:
            print("[INFO] Computing metrics...")
            db_client.compute_metrics()
            print("[INFO] Done. Sleeping...")
        except Exception as e:
            print(f"[ERROR] metrics job failed: {e}")

        time.sleep(INTERVAL_SECONDS)
