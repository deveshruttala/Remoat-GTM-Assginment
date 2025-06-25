import os
import psycopg2
import time
from dotenv import load_dotenv
load_dotenv()

def connect_to_db(retries=10, delay=3):
    for attempt in range(retries):
        try:
            print(f"[DB] Attempt {attempt + 1} to connect to PostgreSQL...")
            conn = psycopg2.connect(
                dbname=os.getenv('POSTGRES_DB'),
                user=os.getenv('POSTGRES_USER'),
                password=os.getenv('POSTGRES_PASSWORD'),
                host=os.getenv('POSTGRES_HOST')
            )
            print("[DB] Connection successful.")
            return conn
        except psycopg2.OperationalError as e:
            print(f"[DB] Connection failed: {e}")
            time.sleep(delay)
    raise Exception("[DB] Could not connect to the database after retries.")

def init_db():
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS stories (
            id SERIAL PRIMARY KEY,
            headline TEXT
        );
    """)
    conn.commit()
    cur.close()
    conn.close()
    print("[DB] Initialized or verified 'stories' table.")

def save_stories(stories):
    conn = connect_to_db()
    cur = conn.cursor()
    for s in stories:
        cur.execute("INSERT INTO stories (headline) VALUES (%s);", (s,))
    conn.commit()
    cur.close()
    conn.close()
    print(f"[DB] Saved {len(stories)} stories.")
