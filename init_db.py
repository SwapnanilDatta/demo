import os
import psycopg2
from dotenv import load_dotenv


load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

def init_db():
    if not DATABASE_URL:
        print("Error: DATABASE_URL is not set in your .env file.")
        return

    print("Connecting to the database...")
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()

        print("Reading schema.sql...")
        with open('schema.sql', 'r') as f:
            schema_script = f.read()

        print("Executing schema setup...")
        cur.execute(schema_script)
        
        conn.commit()
        print("Successfully created the tables!")

    except Exception as e:
        print(f"Failed to create tables: {e}")
    finally:
        if 'cur' in locals(): cur.close()
        if 'conn' in locals(): conn.close()

if __name__ == '__main__':
    init_db()
