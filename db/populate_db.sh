#!/bin/bash
echo "Starting populate_db.sh"
echo "Python version:"
python3 --version
echo "Current directory:"
pwd
echo "Contents of /data:"
ls -l /data
echo "Contents of /docker-entrypoint-initdb.d/:"
ls -l /docker-entrypoint-initdb.d/
echo "Running Python script:"
python3 -u <<EOF
import json
import psycopg2
import os
import sys

print("Python script started", flush=True)

def load_json(file_path):
    print(f"Attempting to load JSON from {file_path}", flush=True)
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        print(f"Successfully loaded JSON from {file_path}", flush=True)
        return data
    except Exception as e:
        print(f"Error loading JSON from {file_path}: {str(e)}", flush=True)
        return None

def insert_data(conn, table, data):
    print(f"Attempting to insert data into {table}", flush=True)
    cur = conn.cursor()
    for item in data:
        if table == 'words':
            cur.execute(f"INSERT INTO {table} (word, ai_likelihood) VALUES (%s, %s) ON CONFLICT (word) DO NOTHING", (item['word'], item['ai_likelihood']))
        elif table == 'phrases':
            cur.execute(f"INSERT INTO {table} (phrase, ai_likelihood) VALUES (%s, %s) ON CONFLICT (phrase) DO NOTHING", (item['phrase'], item['ai_likelihood']))
    conn.commit()
    cur.close()
    print(f"Data insertion into {table} completed", flush=True)

def main():
    print("Starting database population script", flush=True)
    print(f"Current working directory: {os.getcwd()}", flush=True)
    print(f"Environment variables: {os.environ}", flush=True)
    
    try:
        conn = psycopg2.connect(
            dbname=os.environ['POSTGRES_DB'],
            user=os.environ['POSTGRES_USER'],
            password=os.environ['POSTGRES_PASSWORD'],
            host="localhost"
        )
        print("Successfully connected to the database", flush=True)
    except Exception as e:
        print(f"Error connecting to the database: {str(e)}", flush=True)
        sys.exit(1)

    words = load_json('/data/words.json')
    phrases = load_json('/data/phrases.json')

    if words and phrases:
        insert_data(conn, 'words', words['words'])
        insert_data(conn, 'phrases', phrases['phrases'])

    conn.close()
    print("Database population completed", flush=True)

if __name__ == "__main__":
    main()
EOF
echo "populate_db.sh completed"