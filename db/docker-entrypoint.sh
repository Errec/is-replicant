#!/bin/bash
set -e

# Function to output messages with timestamps
log() {
    echo "$(date +"%Y-%m-%d %T") - $1"
}

log "Starting PostgreSQL..."

# Run the original PostgreSQL entrypoint script in the background
/usr/local/bin/docker-entrypoint.sh postgres &

# Wait for PostgreSQL to be ready
log "Waiting for PostgreSQL to be ready..."
until pg_isready -U "$POSTGRES_USER" -d "$POSTGRES_DB"; do
  sleep 1
done

log "PostgreSQL is ready. Running populate_db.py..."

# Activate the virtual environment and run the populate script
. /opt/venv/bin/activate && \
python3 /docker-entrypoint-initdb.d/populate_db.py

log "populate_db.py has completed. PostgreSQL setup is complete."

# Keep the container running
wait
