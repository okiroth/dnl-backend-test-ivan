FROM postgres

COPY DB_SCHEMA.sql /docker-entrypoint-initdb.d/

ENV POSTGRES_USER=ivan
ENV POSTGRES_PASSWORD=some123
ENV POSTGRES_DB=urparts

# RUN ["/usr/local/bin/docker-entrypoint.sh", "postgres"]

