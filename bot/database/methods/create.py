import mysql.connector # type: ignore
import logging
from ..db_connector import create_connection, DB_CONFIG
import json



# Функция для сохранения данных пользователя в базе данных
async def save_user_data(tgid, birthday, username, location):
    try:
        conn = create_connection()
        cursor = conn.cursor()

        query = "INSERT INTO users (tgid, birthday, tgusername, location) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (tgid, birthday, username, location))

        conn.commit()
    except mysql.connector.Error as err:
        logging.error("Error while saving user data: %s", err)
    finally:
        cursor.close()
        conn.close()