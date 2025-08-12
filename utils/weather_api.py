# -*- coding: utf-8 -*-
"""
Utility for fetching data from the OpenWeatherMap API.
"""
import requests
from utils.logger import get_logger
from utils.redis_utils import get_cache, set_cache
from config import OWM_API_KEY

logger = get_logger(__name__)
OWM_API_URL = "http://api.openweathermap.org/data/2.5/weather"
WEATHER_CACHE_TTL = 30 * 60 # Cache for 30 minutes

def get_weather(city: str) -> dict | None:
    """
    Fetches the current weather for a given city.

    Args:
        city: The name of the city.

    Returns:
        A dictionary containing formatted weather data, or None on error.
    """
    cache_key = f"weather:{city.lower()}"

    # 1. Check cache
    cached_weather = get_cache(cache_key)
    if cached_weather:
        logger.info(f"Cache hit for weather in {city}")
        return cached_weather

    # 2. Fetch from API
    if not OWM_API_KEY:
        logger.warning("OWM_API_KEY is not set. Cannot fetch weather.")
        return None

    params = {
        'q': city,
        'appid': OWM_API_KEY,
        'units': 'metric' # Get temperature in Celsius
    }

    try:
        response = requests.get(OWM_API_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Extract relevant information
        weather_info = {
            'city': data.get('name'),
            'description': data['weather'][0]['description'].capitalize(),
            'icon': data['weather'][0]['main'], # e.g., Clouds, Rain, Clear
            'temp': data['main']['temp'],
            'feels_like': data['main']['feels_like'],
            'humidity': data['main']['humidity'],
            'wind_speed': data['wind']['speed'] # in meter/sec
        }

        # Map icon to emoji
        icon_map = {
            "Clear": "☀️", "Clouds": "☁️", "Rain": "🌧️",
            "Drizzle": "🌦️", "Thunderstorm": "⛈️", "Snow": "❄️",
            "Mist": "🌫️", "Fog": "🌫️"
        }
        weather_info['emoji'] = icon_map.get(weather_info['icon'], "🌡️")

        # 3. Set cache
        set_cache(cache_key, weather_info, ttl=WEATHER_CACHE_TTL)

        return weather_info

    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching weather for {city}: {e}")
        if e.response and e.response.status_code == 404:
            return {"error": "city_not_found"}
        return None
    except (ValueError, KeyError) as e:
        logger.error(f"Error parsing weather data for {city}: {e}")
        return None
