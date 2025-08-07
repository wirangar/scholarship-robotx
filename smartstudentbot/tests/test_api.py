import pytest
from unittest.mock import patch, AsyncMock
from fastapi.testclient import TestClient

# Must be imported before the app to ensure patches are applied
from main import app, WEBHOOK_PATH

client = TestClient(app)

def test_health_check():
    """
    Tests the root health check endpoint.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "bot_id": "perugia"}

@patch("aiogram.Dispatcher.feed_update", new_callable=AsyncMock)
def test_webhook_handler(mock_feed_update):
    """
    Tests that the webhook endpoint correctly receives updates and
    returns a 200 OK status. It mocks the dispatcher to prevent
    full update processing.
    """
    # A sample update payload from Telegram
    sample_update = {
        "update_id": 10000,
        "message": {
            "message_id": 1365,
            "from": {
                "id": 123456789,
                "is_bot": False,
                "first_name": "John",
                "last_name": "Doe",
                "username": "johndoe",
                "language_code": "en"
            },
            "chat": {
                "id": 123456789,
                "type": "private",
                "first_name": "John",
                "last_name": "Doe",
                "username": "johndoe"
            },
            "date": 1603271442,
            "text": "/start"
        }
    }

    response = client.post(WEBHOOK_PATH, json=sample_update)

    # Assert that the webhook endpoint acknowledged the request successfully
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

    # Assert that the dispatcher's feed_update method was called
    mock_feed_update.assert_called_once()
    # The first argument is the bot instance, the second is the update
    called_update = mock_feed_update.call_args.kwargs['update']
    assert called_update.update_id == sample_update['update_id']
