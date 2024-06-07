from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from dotenv import load_dotenv
from page_analyzer.validator import validate
from page_analyzer.normalizer import normalize
from datetime import datetime
import psycopg2
import os

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

DATABASE_URL = os.getenv('DATABASE_URL')
conn = psycopg2.connect(DATABASE_URL)


@app.route('/')
def main_page():
    return render_template('main_page.html')


@app.route('/urls')
def get_urls():
    with conn.cursor as curs:
        curs.execute('SELECT * FROM urls')
        urls = curs.fetchall()

    return render_template(
        'index.html',
        urls=urls,
    )


@app.route('/urls', methods=['POST'])
def post_url():
    with conn.cursor as curs:
        curs.execute('SELECT * FROM urls')
        urls = curs.fetchall()
    user_url = request.form.to_dict()['url']
    normalized_url = normalize(user_url)

    error = validate(normalized_url)
    if error:
        flash(error, 'danger')
        return render_template(
            'main_page.html',
            url=user_url,
        ), 422

    url_id = PLACEHOLDER_find_id(normalized_url)
    if url_id:
        flash('Страница уже существует', 'warning')
        return redirect(url_for('get_url', id=url_id))

    with conn.cursor as curs:
        current_date = datetime.now().date()
        curs.execute(f'INSERT INTO urls (name, created_at) VALUES (%s, %s), ({normalized_url}, {current_date})')
    flash('Страница успешно добавлена', 'success')
    return redirect(url_for('get_url', id=url_id))


@app.route('/urls/<int:id>')
def get_url(id):
    with conn.cursor as curs:
        curs.execute('SELECT * FROM urls')
        urls = curs.fetchall()
    url = urls.PLACEHOLDER_find(id)

    if not url:
        return 'Page not found', 404

    return render_template(
        'show.html',
        url=url,
    )
