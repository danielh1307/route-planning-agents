import requests

from src.route.route_tools import Point
from langchain_core.tools import tool

@tool
def get_weather(date: str, point: Point) -> dict:
    """This function returns weather data for a specific date and a point with a latitude and longitude.
    date must be given in the format YYYY-MM-DD.
    """
    url = f"https://api.open-meteo.com/v1/forecast?latitude={point.lat}&longitude={point.lng}&hourly=precipitation_probability,temperature_2m&start_date={date}&end_date={date}"

    response = requests.get(url)
    data = response.json()

    # Filter to every third hour
    filtered_data = {
        "time": data["hourly"]["time"][::3],
        "precipitation_probability": data["hourly"]["precipitation_probability"][::3],
        "temperature_2m": data["hourly"]["temperature_2m"][::3]
    }

    return filtered_data

#print(get_weather("2024-11-01", "2024-11-01", Point(lat=47.01, lng=8.03)))
