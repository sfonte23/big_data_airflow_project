import os
import json
import sqlite3
from datetime import datetime

INPUT_FILE = os.path.join("data", "raw", "raw_users_with_error.json")
DB_PATH = os.path.join("data", "bronze", "users_bronze.db")

def create_bronze_table(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users_bronze (
            id TEXT PRIMARY KEY,
            name TEXT,
            email TEXT,
            address TEXT,
            phone_number TEXT,
            birth_date TEXT,
            cpf TEXT,
            registration_timestamp_utc TEXT,
            ingestion_timestamp TEXT
        )
    ''')
    conn.commit()

def load_json_to_sqlite():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        users_data = json.load(f)

    conn = sqlite3.connect(DB_PATH)

    try:
        create_bronze_table(conn)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users_bronze")
        ingestion_time = datetime.utcnow().isoformat() + "Z"

        for user in users_data:
            cursor.execute('''
                INSERT OR IGNORE INTO users_bronze
                (id, name, email, address, phone_number, birth_date, cpf,
                 registration_timestamp_utc, ingestion_timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                user.get('id'),
                user.get('name'),
                user.get('email'),
                user.get('address'),
                user.get('phone_number'),
                user.get('birth_date'),
                user.get('cpf'),
                user.get('registration_timestamp_utc'),
                ingestion_time
            ))

        conn.commit()
        print(f"Successfully loaded {len(users_data)} users into bronze layer: {DB_PATH}")

    except Exception as e:
        print(f"Error loading data: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    load_json_to_sqlite()
