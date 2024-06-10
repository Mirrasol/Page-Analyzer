from dotenv import load_dotenv
import os
import psycopg2

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')


def open_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn
