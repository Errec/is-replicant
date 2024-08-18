FROM postgres:13

# Install Python and psycopg2
RUN apt-get update && apt-get install -y python3 python3-psycopg2

COPY init.sql /docker-entrypoint-initdb.d/
COPY populate_db.py /docker-entrypoint-initdb.d/
COPY data /data

# Make the script executable
RUN chmod +x /docker-entrypoint-initdb.d/populate_db.py