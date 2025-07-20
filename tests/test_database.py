import unittest
import os
from unittest.mock import patch, MagicMock
# It's good practice to load .env in tests if you're depending on it
from dotenv import load_dotenv
load_dotenv()

# We need to import the module we are testing *after* loading the env vars
import database

class TestDatabase(unittest.TestCase):

    @patch('database.psycopg2.connect')
    def test_initialize_db_creates_table(self, mock_connect):
        """
        Tests that initialize_db function executes the correct SQL commands
        to create the 'users' table and the associated trigger.
        """
        # Ensure DATABASE_URL is set for the test environment
        os.environ['DATABASE_URL'] = 'postgresql://test:test@localhost/testdb'

        # Mock the connection and cursor objects
        mock_conn = MagicMock()
        mock_cur = MagicMock()

        # Set up the context manager behavior for the cursor
        mock_conn.cursor.return_value.__enter__.return_value = mock_cur
        mock_connect.return_value = mock_conn

        # Call the function
        database.initialize_db()

        # Assert that connect was called with the correct DATABASE_URL
        mock_connect.assert_called_with(os.environ['DATABASE_URL'])

        # Check that the cursor was created
        mock_conn.cursor.assert_called_once()

        # Check the executed SQL commands by inspecting the call args
        execute_calls = [call[0][0] for call in mock_cur.execute.call_args_list]

        self.assertTrue(any("CREATE TABLE IF NOT EXISTS users" in call for call in execute_calls))
        self.assertTrue(any("CREATE OR REPLACE FUNCTION update_updated_at_column()" in call for call in execute_calls))
        self.assertTrue(any("CREATE TRIGGER update_users_updated_at" in call for call in execute_calls))

        # Assert that commit was called and the connection was closed
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()

    def tearDown(self):
        # Clean up environment variable after test
        if 'DATABASE_URL' in os.environ:
            del os.environ['DATABASE_URL']

if __name__ == '__main__':
    unittest.main()
