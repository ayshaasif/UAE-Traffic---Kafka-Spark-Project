from tomtom_client import get_traffic
import time

# Example: Sheikh Zayed Road (approx)
LAT = 25.2048
LON = 55.2708

while True:
    data = get_traffic(LAT, LON)

    if data:
        print("\n--- Traffic Snapshot ---")
        print(data)

    time.sleep(60)
    