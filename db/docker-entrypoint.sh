#!/bin/bash
set -e

# Run the original PostgreSQL entrypoint script
/usr/local/bin/docker-entrypoint.sh postgres &

# Wait for PostgreSQL to be ready
until pg_isready -U "$POSTGRES_USER" -d "$POSTGRES_DB"; do
  sleep 1
done

echo "PostgreSQL is ready. Running populate_db.py..."

# Activate virtual environment and run the populate script
. /opt/venv/bin/activate && \
python3 /docker-entrypoint-initdb.d/populate_db.py

# Keep the container running
wait