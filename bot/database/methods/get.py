import mysql.connector # type: ignore
import logging
from ..db_connector import create_connection
import json

# Функция для получения списка дней рождения пользователей
async def get_birthdays():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)

        query = "SELECT tgusername, birthday FROM users"
        cursor.execute(query)

        return cursor.fetchall()
    except mysql.connector.Error as err:
        logging.error("Error while getting birthdays: %s", err)
        return None
    finally:
        cursor.close()
        conn.close()

