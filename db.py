import os
import psycopg2

def get_db_connection():
    """Establishes and returns a connection to the PostgreSQL database."""
    DATABASE_URL = os.getenv('DATABASE_URL')
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL is not set in environment variables.")
    
    conn = psycopg2.connect(DATABASE_URL)
    return conn
