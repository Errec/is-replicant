FROM postgres:13

# Install Python and psycopg2
RUN apt-get update && apt-get install -y python3 python3-psycopg2

COPY init.sql /docker-entrypoint-initdb.d/
COPY populate_db.sh /docker-entrypoint-initdb.d/
RUN chmod +x /docker-entrypoint-initdb.d/populate_db.sh
COPY data /data

# Copy and set permissions for the new entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Use the new entrypoint script
ENTRYPOINT ["/entrypoint.sh"]