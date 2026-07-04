#!/usr/bin/env python3
import sqlite3
from requests import get

# Define the URL of the API you want to monitor (example: news API)
API_URL = "https://newsapi.org/v2/top-headlines?country=US"

# Connect to SQLite database
db_conn = sqlite3.connect("/Users/savage-p.c./Projects/active/jarvishive/jarvis_accounting.db")
db_cursor = db_conn.cursor()

# Create table if it doesn't exist
db_cursor.execute('''
    CREATE TABLE IF NOT EXISTS jarvis_business_logs (
        directive_executed TEXT,
        raw_payload BLOB
    )
''')

# Function to log the operation and payload
def log_operation(payload):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    db_cursor.execute('''
        INSERT INTO jarvis_business_logs (directive_executed, raw_payload)
        VALUES (?, ?)
    ''', (now, payload))
    db_conn.commit()

# Main loop
while True:
    # Fetch the data from the API
    try:
        response = get(API_URL)

        if response.status_code == 200:
            data = response.json()
            log_operation(json.dumps(data))
            print("Data fetched successfully")
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")
    
    except Exception as e:
        print(f"An error occurred: {e}")

    # Sleep for 60 seconds before the next loop iteration
    time.sleep(60)

db_conn.close()