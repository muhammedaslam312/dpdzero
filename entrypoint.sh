#!/bin/bash
# entrypoint.sh

function check_postgres {
    python - <<END
import os
import psycopg2
import time

db_host = os.environ["DB_HOST"]
db_port = int(os.environ["DB_PORT"])

while True:
    try:
        conn = psycopg2.connect(
            dbname=os.environ["DB_NAME"],
            user=os.environ["DB_USER"],
            password=os.environ["DB_PASSWORD"],
            host=db_host,
            port=db_port,
        )
        conn.close()
        print("PostgreSQL is ready.")
        break
    except psycopg2.OperationalError as e:
        print(f"Waiting for PostgreSQL to be ready... {e}")
        time.sleep(2)
END
}


# Wait for the PostgreSQL container to be ready
check_postgres

# Apply migrations
python manage.py migrate

# Start the development server
python manage.py runserver 0.0.0.0:8000
