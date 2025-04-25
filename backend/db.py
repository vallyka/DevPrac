import psycopg2
import os
import time

def get_connection(retries=5):
    for i in range(retries):
        try:
            return psycopg2.connect(
                dbname=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASS"),
                host=os.getenv("DB_HOST"),
                port=os.getenv("DB_PORT")
            )
        except psycopg2.OperationalError:
            print("База недоступна, пробую снова...")
            time.sleep(2)
    raise Exception("Не удалось подключиться к базе данных")