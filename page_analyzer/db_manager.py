from datetime import datetime
from psycopg2.extras import NamedTupleCursor
import os
import psycopg2

DATABASE_URL = os.getenv('DATABASE_URL')


def open_connection():
    """Open connection to the database."""
    conn = psycopg2.connect(DATABASE_URL)
    return conn


def get_urls_data():
    """Get all data from the table: urls."""
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


def get_url_id(url_name):
    """Get the id of the given url name."""
    with open_connection() as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
            curs.execute(
                "SELECT * FROM urls WHERE name = %s;",
                (url_name,)
            )
            url_data = curs.fetchone()
            url_id = url_data.id if url_data else None
    return url_id


def add_new_url(url_name):
    """Add new entry to the table: urls."""
    with open_connection() as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
            current_date = datetime.now().date()
            curs.execute(
                "INSERT INTO urls (name, created_at) VALUES (%s, %s);",
                (url_name, current_date)
            )


def get_url_data(url_id):
    """Get all data on the given url id from the table: urls."""
    with open_connection() as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
            curs.execute("SELECT * FROM urls WHERE id = %s;", (url_id,))
            url_data = curs.fetchone()
    return url_data


def get_url_checks(url_id):
    """Get all checks of the given url id from the table: urls_checks."""
    with open_connection() as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
            curs.execute("SELECT * FROM urls_checks\
                WHERE url_id = %s\
                ORDER BY id DESC;", (url_id,))
            checks = curs.fetchall()
    return checks


def add_new_check(id, status_code, h1, title, description, date):
    """Add new entry to the table: urls_checks."""
    with open_connection() as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
            curs.execute(
                "INSERT INTO urls_checks (\
                url_id,\
                status_code,\
                h1,\
                title,\
                description,\
                created_at\
                )\
                VALUES (%s, %s, %s, %s, %s, %s);",
                (id, status_code, h1, title, description, date)
            )
