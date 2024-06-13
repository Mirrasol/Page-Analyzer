from datetime import datetime
from dotenv import load_dotenv
from psycopg2.extras import NamedTupleCursor
import os
import psycopg2

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')


def open_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn


def get_urls_data():
    with open_connection() as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
            curs.execute("SELECT\
            urls.id AS id,\
            urls.name AS name,\
            urls_checks.status_code AS status_code,\
            MAX(urls_checks.created_at) AS created_at\
            FROM urls\
            LEFT JOIN urls_checks ON urls.id = urls_checks.url_id\
            GROUP BY urls.id, urls.name, urls_checks.status_code\
            ORDER BY urls.id DESC;")
            urls_data = curs.fetchall()
    return urls_data


def find_url(url_name):
    with open_connection() as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
            curs.execute(
                "SELECT * FROM urls WHERE name = %s;",
                (url_name,)
            )
            url_data = curs.fetchone()
    return url_data


def post_new_url(url_name):
    with open_connection() as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
            current_date = datetime.now().date()
            curs.execute(
                "INSERT INTO urls (name, created_at) VALUES (%s, %s);",
                (url_name, current_date)
            )
