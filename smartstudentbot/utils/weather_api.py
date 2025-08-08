import httpx
from config import OPENWEATHERMAP_API_KEY
from utils.logger import logger

BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

async def get_current_weather(city: str) -> str:
    """
    Fetches the current weather for a given city from the OpenWeatherMap API.
    Returns a formatted string with the weather information or an error message.
    """
    if not OPENWEATHERMAP_API_KEY:
        logger.warning("OpenWeatherMap API key is not set.")
        return "Sorry, the weather service is not configured."

    params = {
        "q": city,
        "appid": OPENWEATHERMAP_API_KEY,
        "units": "metric"  # For Celsius
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(BASE_URL, params=params)
            response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

            data = response.json()

            weather_desc = data['weather'][0]['description'].capitalize()
            temp = data['main']['temp']
            feels_like = data['main']['feels_like']
            humidity = data['main']['humidity']
            wind_speed = data['wind']['speed']
            city_name = data['name']

            # Simple emoji mapping
            emoji = "❓"
            if "clear" in weather_desc.lower(): emoji = "☀️"
            elif "clouds" in weather_desc.lower(): emoji = "☁️"
            elif "rain" in weather_desc.lower(): emoji = "🌧️"
            elif "snow" in weather_desc.lower(): emoji = "❄️"
            elif "thunderstorm" in weather_desc.lower(): emoji = "⛈️"
            elif "mist" in weather_desc.lower() or "fog" in weather_desc.lower(): emoji = "🌫️"

            return (
                f"**Weather in {city_name}** {emoji}\n\n"
                f"🌡️ **Temperature:** {temp}°C\n"
                f"🤔 **Feels like:** {feels_like}°C\n"
                f"💧 **Humidity:** {humidity}%\n"
                f"💨 **Wind:** {wind_speed} m/s\n"
                f"📋 **Condition:** {weather_desc}"
            )

    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            logger.error(f"Weather API error: City '{city}' not found.")
            return f"Sorry, I couldn't find the city '{city}'."
        else:
            logger.error(f"Weather API error: {e}")
            return "Sorry, there was an error fetching the weather data."
    except Exception as e:
        logger.error(f"An unexpected error occurred in get_current_weather: {e}")
        return "An unexpected error occurred."
