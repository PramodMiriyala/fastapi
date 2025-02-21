import requests
import os
from dotenv import load_dotenv

load_dotenv()

def get_weather(lat, lon):
    base_url = "http://api.weatherapi.com/v1"
    current_weather_endpoint = "/current.json"
    query = f"{lat},{lon}"
    auth = os.getenv("KEY")
    if not auth:
        return {"error": "API key is missing. Please check your .env file."}
    URL = f"{base_url}{current_weather_endpoint}?key={auth}&q={query}"
    try:
        response = requests.get(URL, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        return f"error: {str(e)}"

if __name__ == "__main__":
    print(get_weather(16.703285,81.100388))

# 16.703285,81.100388