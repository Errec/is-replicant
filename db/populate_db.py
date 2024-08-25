"""Module to populate the database with the words and phrases data from the JSON files."""
from contextlib import contextmanager
import json
import os
import time
import logging
import psycopg2
from psycopg2 import OperationalError, sql

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@contextmanager
def get_db_connection():
    """Context manager for database connection."""
    conn = None
    try:
        conn = psycopg2.connect(
            dbname=os.environ['POSTGRES_DB'],
            user=os.environ['POSTGRES_USER'],
            password=os.environ['POSTGRES_PASSWORD'],
            host=os.environ.get('POSTGRES_HOST', 'localhost')  # Use 'localhost' if POSTGRES_HOST is not set
        )
        yield conn
    except OperationalError as e:
        logging.error("Database connection failed: %s", e)
        raise
    finally:
        if conn:
            conn.close()

def load_json(file_path):
    """Load JSON data from a file."""
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        logging.error("Failed to load JSON file %s: %s", file_path, e)
        raise

def insert_data(conn, table, data):
    """Insert data into the database."""
    cur = conn.cursor()
    try:
        for item in data:
            if table == 'words':
                cur.execute(
                    sql.SQL("INSERT INTO {table} (word, ai_likelihood) VALUES (%s, %s) ON CONFLICT (word) DO NOTHING")
                    .format(table=sql.Identifier(table)),
                    (item['word'], item['ai_likelihood'])
                )
            elif table == 'phrases':
                cur.execute(
                    sql.SQL("INSERT INTO {table} (phrase, ai_likelihood) VALUES (%s, %s) ON CONFLICT (phrase) DO NOTHING")
                    .format(table=sql.Identifier(table)),
                    (item['phrase'], item['ai_likelihood'])
                )
        conn.commit()
    except Exception as e:
        conn.rollback()
        logging.error("Failed to insert data into table %s: %s", table, e)
        raise
    finally:
        cur.close()

def main():
    """Main function to populate the database."""
    retry_count = 0
    max_retries = 5
    while retry_count < max_retries:
        try:
            with get_db_connection() as conn:
                words = load_json('/data/words.json')
                phrases = load_json('/data/phrases.json')

                insert_data(conn, 'words', words['words'])
                insert_data(conn, 'phrases', phrases['phrases'])
                logging.info("Database population completed successfully")
                break
        except OperationalError:
            retry_count += 1
            logging.warning("Waiting for database to be ready... Attempt %d of %d", retry_count, max_retries)
            time.sleep(2)
        except Exception as e:
            logging.error("An error occurred: %s", e)
            break
    else:
        logging.error("Max retries reached. Could not connect to the database.")

if __name__ == "__main__":
    main()
