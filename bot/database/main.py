import mysql.connector # type: ignore
import logging
import json

logging.basicConfig(level=logging.INFO)


DB_CONFIG={
        'host': '127.0.0.1',
        'user': 'root',
        'password': 'q1q1q1q1',
        'database': 'rassvet'
}

# Соединение с БД
async def create_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as e:
        logging.error(f"Error connecting to MySQL: {e}")
        return None
