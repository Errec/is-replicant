FROM postgres:13

# Install Python and venv
RUN apt-get update && apt-get install -y \
    python3 \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*

# Create a virtual environment
RUN python3 -m venv /opt/venv

# Activate virtual environment and install psycopg2-binary
RUN . /opt/venv/bin/activate && \
    pip install psycopg2-binary

COPY init.sql /docker-entrypoint-initdb.d/
COPY populate_db.py /docker-entrypoint-initdb.d/
COPY data /data

# Copy and set permissions for the new entrypoint script
COPY docker-entrypoint.sh /usr/local/bin/custom-entrypoint.sh
RUN chmod +x /usr/local/bin/custom-entrypoint.sh

ENTRYPOINT ["/usr/local/bin/custom-entrypoint.sh"]