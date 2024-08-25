import json
import psycopg2
import os
import time

def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def insert_data(conn, table, data):
    cur = conn.cursor()
    for item in data:
        if table == 'words':
            cur.execute(f"INSERT INTO {table} (word, ai_likelihood) VALUES (%s, %s) ON CONFLICT (word) DO NOTHING", (item['word'], item['ai_likelihood']))
        elif table == 'phrases':
            cur.execute(f"INSERT INTO {table} (phrase, ai_likelihood) VALUES (%s, %s) ON CONFLICT (phrase) DO NOTHING", (item['phrase'], item['ai_likelihood']))
    conn.commit()
    cur.close()

def main():
    while True:
        try:
            conn = psycopg2.connect(
                dbname=os.environ['POSTGRES_DB'],
                user=os.environ['POSTGRES_USER'],
                password=os.environ['POSTGRES_PASSWORD'],
                host="localhost"
            )
            break
        except psycopg2.OperationalError:
            print("Waiting for database to be ready...")
            time.sleep(2)

    words = load_json('/data/words.json')
    phrases = load_json('/data/phrases.json')

    insert_data(conn, 'words', words['words'])
    insert_data(conn, 'phrases', phrases['phrases'])

    conn.close()
    print("Database population completed")

if __name__ == "__main__":
    main()