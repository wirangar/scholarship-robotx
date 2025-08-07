# SmartStudentBot

Welcome to the SmartStudentBot project! This is a Telegram bot designed to assist students in Perugia.

## Project Structure

- `main.py`: The main entry point for the FastAPI application and bot webhook.
- `config.py`: Handles configuration and environment variables.
- `handlers/`: Contains all the logic for handling Telegram commands and messages.
- `utils/`: A package for utility functions (database, logging, etc.).
- `ai/`: Contains modules related to Artificial Intelligence features.
- `tests/`: Contains all the tests for the project.
- `lang/`: JSON files for internationalization (i18n).
- `requirements.in`: Main application dependencies.
- `dev-requirements.in`: Development-specific dependencies.

## Local Development

1.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

2.  **Install dependencies:**
    ```bash
    pip install pip-tools
    pip-compile requirements.in
    pip-compile dev-requirements.in
    pip install -r requirements.txt -r dev-requirements.txt
    ```

3.  **Set up your environment:**
    - Copy the `.env.example` file to `.env` and fill in your local configuration details.

4.  **Run the application:**
    The application will run using uvicorn. It will be started from the `smartstudentbot` directory.
    ```bash
    cd smartstudentbot
    uvicorn main:app --reload
    ```

## Testing

To run the test suite, use pytest:

```bash
python -m pytest
```
