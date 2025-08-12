# -*- coding: utf-8 -*-
"""
Redis utility functions for caching, rate limiting, and queues.
"""
import redis
import json
from config import REDIS_URL
from utils.logger import get_logger

logger = get_logger(__name__)

try:
    # Use from_url for easy connection to services like Upstash
    redis_client = redis.from_url(REDIS_URL, decode_responses=True)
    redis_client.ping()
    logger.info("Successfully connected to Redis.")
except redis.exceptions.ConnectionError as e:
    logger.error(f"Could not connect to Redis: {e}")
    # In a real app, you might want to exit or have a fallback mechanism.
    # For this implementation, we'll let it fail and log errors on use.
    redis_client = None

# --- Caching ---

def get_cache(key: str):
    """
    Gets a value from the Redis cache.
    Returns None if the key does not exist or Redis is unavailable.
    """
    if not redis_client:
        return None
    try:
        value = redis_client.get(key)
        return json.loads(value) if value else None
    except Exception as e:
        logger.error(f"Error getting cache for key '{key}': {e}")
        return None

def set_cache(key: str, value, ttl: int):
    """
    Sets a value in the Redis cache with a TTL in seconds.
    The value will be JSON serialized.
    """
    if not redis_client:
        return
    try:
        serialized_value = json.dumps(value)
        redis_client.set(key, serialized_value, ex=ttl)
    except Exception as e:
        logger.error(f"Error setting cache for key '{key}': {e}")

# --- Rate Limiting ---
# A simple fixed window rate limiter.

RATE_LIMIT_PER_MINUTE = 100
RATE_LIMIT_WINDOW = 60 # seconds

def check_rate_limit(user_id: int) -> bool:
    """
    Checks if a user has exceeded the rate limit.
    Returns True if the user is within limits, False otherwise.
    """
    if not redis_client:
        # If Redis is down, we fail open (allow the request) to not block users.
        return True

    key = f"ratelimit:{user_id}"
    try:
        # Increment the count. If the key doesn't exist, it's created with a value of 1.
        current_count = redis_client.incr(key)

        # Set the expiration only when the key is first created.
        if current_count == 1:
            redis_client.expire(key, RATE_LIMIT_WINDOW)

        if current_count > RATE_LIMIT_PER_MINUTE:
            return False # Limit exceeded

        return True # Within limits
    except Exception as e:
        logger.error(f"Error checking rate limit for user '{user_id}': {e}")
        return True # Fail open

# --- Queueing (Example using ZSET for scheduled tasks) ---
# This can be used for reminders or other scheduled actions.

SCHEDULE_QUEUE_KEY = "queue:schedule"

def schedule_task(timestamp: int, task_data: dict):
    """
    Schedules a task to be run at a specific UNIX timestamp.
    `task_data` should be a JSON-serializable dictionary.
    """
    if not redis_client:
        return
    try:
        member = json.dumps(task_data)
        redis_client.zadd(SCHEDULE_QUEUE_KEY, {member: timestamp})
        logger.info(f"Scheduled task at {timestamp}: {task_data}")
    except Exception as e:
        logger.error(f"Error scheduling task: {e}")

def get_due_tasks(timestamp: int):
    """
    Retrieves all tasks that are due to be run at or before the given timestamp.
    """
    if not redis_client:
        return []
    try:
        # Get tasks with scores (timestamps) from 0 up to the current time.
        tasks = redis_client.zrangebyscore(SCHEDULE_QUEUE_KEY, 0, timestamp)
        # For atomicity, you'd typically remove them in the same transaction.
        if tasks:
            redis_client.zremrangebyscore(SCHEDULE_QUEUE_KEY, 0, timestamp)
        return [json.loads(task) for task in tasks]
    except Exception as e:
        logger.error(f"Error getting due tasks: {e}")
        return []
