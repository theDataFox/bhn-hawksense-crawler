FROM postgres:11

# Custom initialization scripts
COPY app/scripts/db-init.sh /docker-entrypoint-initdb.d/20-db-init.sh
COPY app/scripts/schema.sql /schema.sql

RUN chmod +x /docker-entrypoint-initdb.d/20-db-init.sh