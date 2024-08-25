FROM postgres:13

# Install Python and venv
RUN apt-get update && \
    apt-get install -y python3 python3-venv && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create and activate a virtual environment, then install psycopg2-binary
RUN python3 -m venv /opt/venv && \
    /opt/venv/bin/pip install --no-cache-dir psycopg2-binary

# Copy the initialization SQL and Python files
COPY init.sql /docker-entrypoint-initdb.d/
COPY populate_db.py /docker-entrypoint-initdb.d/
COPY data /data

# Copy and set permissions for the custom entrypoint script
COPY docker-entrypoint.sh /usr/local/bin/custom-entrypoint.sh
RUN chmod +x /usr/local/bin/custom-entrypoint.sh

# Use the custom entrypoint script
ENTRYPOINT ["/usr/local/bin/custom-entrypoint.sh"]
