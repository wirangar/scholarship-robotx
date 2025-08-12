# -*- coding: utf-8 -*-
"""
Network utility functions for fetching data from external URLs.
"""
import requests
from utils.logger import get_logger
from utils.redis_utils import get_cache, set_cache
from config import CACHE_TTL_SECONDS

logger = get_logger(__name__)

def fetch_json(url: str, use_cache: bool = True) -> dict | None:
    """
    Fetches JSON data from a URL, with optional caching.

    Args:
        url: The URL to fetch data from.
        use_cache: Whether to use the Redis cache.

    Returns:
        A dictionary with the JSON content, or None if an error occurs.
    """
    cache_key = f"data_cache:{url}"
    if use_cache:
        cached_data = get_cache(cache_key)
        if cached_data:
            logger.info(f"Cache hit for URL: {url}")
            return cached_data

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

        data = response.json()

        if use_cache:
            set_cache(cache_key, data, ttl=CACHE_TTL_SECONDS)
            logger.info(f"Fetched and cached data from URL: {url}")

        return data

    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching data from {url}: {e}")
        return None
    except ValueError as e: # Catches JSON decoding errors
        logger.error(f"Error decoding JSON from {url}: {e}")
        return None
