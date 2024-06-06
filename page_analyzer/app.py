from flask import Flask, render_template, request
from dotenv import load_dotenv
import psycopg2
import os
import datetime
import requests

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
conn = psycopg2.connect(DATABASE_URL)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def index():
    messages = get_flashed_messages(with_categories=True)
    return render_template(
        'index.html',
        messages=messages,
    )


@app.route('/urls')
def get_urls():
    urls = future_get_database()
    messages = get_flashed_messages(with_categories=True)
    return render_template(
        'show.html',
        urls=urls,
        messages=messages,
    )
