import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("TOMTOM_API_KEY")

BASE_URL = "https://api.tomtom.com/traffic/services/4/flowSegmentData/relative0/10/json"


def get_raw_traffic(lat, lon):
    url = f"{BASE_URL}?key={API_KEY}&point={lat},{lon}"

    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"TomTom API Error: {response.text}")

    return response.json()
