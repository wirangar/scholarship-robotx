# -*- coding: utf-8 -*-
"""
Tests for Redis utility functions.
"""
import pytest
import json
from unittest.mock import MagicMock

# This is a bit of a hack to allow mocking the client before it's imported
# In a larger project, dependency injection would be a cleaner approach.
import utils.redis_utils as redis_utils

# Mock the redis_client at the module level
mock_redis = MagicMock()
redis_utils.redis_client = mock_redis


def test_schedule_task():
    """
    Tests that schedule_task calls the redis client's zadd with correct arguments.
    """
    timestamp = 1234567890
    task_data = {"user_id": 123, "action": "remind"}

    redis_utils.schedule_task(timestamp, task_data)

    # Check that zadd was called once
    mock_redis.zadd.assert_called_once()

    # Check the arguments it was called with
    # zadd(SCHEDULE_QUEUE_KEY, {json.dumps(task_data): timestamp})
    args, kwargs = mock_redis.zadd.call_args
    assert args[0] == redis_utils.SCHEDULE_QUEUE_KEY

    expected_member = json.dumps(task_data)
    expected_mapping = {expected_member: timestamp}
    assert args[1] == expected_mapping


def test_get_due_tasks():
    """
    Tests that get_due_tasks calls zrangebyscore and zremrangebyscore correctly.
    """
    timestamp = 1234567890

    # Simulate the return value from redis
    task1 = {"user_id": 1, "action": "test1"}
    task2 = {"user_id": 2, "action": "test2"}
    mock_redis.zrangebyscore.return_value = [json.dumps(task1), json.dumps(task2)]

    due_tasks = redis_utils.get_due_tasks(timestamp)

    # Check that the correct functions were called
    mock_redis.zrangebyscore.assert_called_with(redis_utils.SCHEDULE_QUEUE_KEY, 0, timestamp)
    mock_redis.zremrangebyscore.assert_called_with(redis_utils.SCHEDULE_QUEUE_KEY, 0, timestamp)

    # Check that the returned data is correctly deserialized
    assert due_tasks == [task1, task2]

def test_get_due_tasks_empty():
    """
    Tests that get_due_tasks handles an empty return from redis.
    """
    timestamp = 1234567890
    mock_redis.zrangebyscore.return_value = []

    due_tasks = redis_utils.get_due_tasks(timestamp)

    assert due_tasks == []
    # zremrangebyscore should not be called if there are no tasks
    mock_redis.zremrangebyscore.assert_not_called()

# Reset the mock after each test function in this module to avoid side effects
@pytest.fixture(autouse=True)
def reset_mock():
    mock_redis.reset_mock()
