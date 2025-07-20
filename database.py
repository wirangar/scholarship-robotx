import psycopg2
import logging
from config import DATABASE_URL

logger = logging.getLogger(__name__)

def get_db_connection():
    """Establishes a connection to the database."""
    if not DATABASE_URL:
        logger.error("DATABASE_URL environment variable is not set.")
        return None
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except psycopg2.OperationalError as e:
        logger.error(f"Could not connect to the database: {e}")
        return None

def initialize_db():
    """Initializes the database and creates tables if they don't exist."""
    conn = get_db_connection()
    if conn is None:
        logger.error("Database initialization failed: No connection.")
        return

    try:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id BIGINT PRIMARY KEY,
                    first_name VARCHAR(255),
                    last_name VARCHAR(255),
                    username VARCHAR(255),
                    language_code VARCHAR(10),
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
                );
            """)
            # Create a trigger to automatically update `updated_at`
            cur.execute("""
                CREATE OR REPLACE FUNCTION update_updated_at_column()
                RETURNS TRIGGER AS $$
                BEGIN
                   NEW.updated_at = NOW();
                   RETURN NEW;
                END;
                $$ language 'plpgsql';
            """)
            cur.execute("""
                DROP TRIGGER IF EXISTS update_users_updated_at ON users;
                CREATE TRIGGER update_users_updated_at
                BEFORE UPDATE ON users
                FOR EACH ROW
                EXECUTE FUNCTION update_updated_at_column();
            """)
            conn.commit()
            logger.info("Database initialized successfully. 'users' table and trigger are ready.")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
    finally:
        if conn:
            conn.close()

def upsert_user(user_data):
    """Inserts a new user or updates an existing one."""
    sql = """
        INSERT INTO users (id, first_name, last_name, username, language_code)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (id) DO UPDATE SET
            first_name = EXCLUDED.first_name,
            last_name = EXCLUDED.last_name,
            username = EXCLUDED.username,
            language_code = EXCLUDED.language_code;
    """
    conn = get_db_connection()
    if not conn:
        return
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (
                user_data.id,
                user_data.first_name,
                user_data.last_name,
                user_data.username,
                user_data.language_code
            ))
            conn.commit()
            logger.info(f"Upserted user {user_data.id} ({user_data.username})")
    except Exception as e:
        logger.error(f"Error upserting user {user_data.id}: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    # This allows you to run `python database.py` to set up the tables manually.
    logger.info("Manual database initialization...")
    initialize_db()
