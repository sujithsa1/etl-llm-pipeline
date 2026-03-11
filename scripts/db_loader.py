import os
import csv
import psycopg2
from psycopg2.extras import execute_batch
import os

DB_CONFIG = {
    "host": os.environ.get("POSTGRES_HOST", "localhost"),
    "port": int(os.environ.get("POSTGRES_PORT", "5432")),
    "database": "etldb",
    "user": "etluser",
    "password": "etlpassword"
}

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS customers (
    id          INTEGER PRIMARY KEY,
    first_name  VARCHAR(100),
    last_name   VARCHAR(100),
    email       VARCHAR(200),
    phone       VARCHAR(50),
    street      VARCHAR(200),
    city        VARCHAR(100),
    state       CHAR(2),
    zip         VARCHAR(10),
    loaded_at   TIMESTAMP DEFAULT NOW()
);
"""

INSERT_SQL = """
INSERT INTO customers (id, first_name, last_name, email, phone, street, city, state, zip)
VALUES (%(id)s, %(first_name)s, %(last_name)s, %(email)s, %(phone)s, %(street)s, %(city)s, %(state)s, %(zip)s)
ON CONFLICT (id) DO UPDATE SET
    first_name = EXCLUDED.first_name,
    last_name  = EXCLUDED.last_name,
    email      = EXCLUDED.email,
    phone      = EXCLUDED.phone,
    street     = EXCLUDED.street,
    city       = EXCLUDED.city,
    state      = EXCLUDED.state,
    zip        = EXCLUDED.zip,
    loaded_at  = NOW();
"""

def load_cleaned_data(filepath: str):
    print(f"📂 Reading cleaned data from {filepath}...")
    with open(filepath, newline="") as f:
        rows = list(csv.DictReader(f))
    print(f"   Found {len(rows)} records")

    print("🔌 Connecting to PostgreSQL...")
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    print("🏗️  Creating table if not exists...")
    cur.execute(CREATE_TABLE_SQL)
    conn.commit()

    print("📤 Loading records into database...")
    execute_batch(cur, INSERT_SQL, rows)
    conn.commit()

    # Verify
    cur.execute("SELECT COUNT(*) FROM customers;")
    count = cur.fetchone()[0]

    cur.close()
    conn.close()

    print(f"✅ Successfully loaded {count} records into customers table")
    return count

if __name__ == "__main__":
    load_cleaned_data("data/cleaned/customers_cleaned.csv")