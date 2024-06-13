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
            urls = curs.fetchall()
            return urls


def post_url_data():
    pass