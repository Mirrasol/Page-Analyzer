from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from bs4 import BeautifulSoup
from datetime import datetime
from page_analyzer.db_manager import (
    get_urls_data,
    open_connection,
)
from page_analyzer.normalizer import normalize
from page_analyzer.validator import validate
from psycopg2.extras import NamedTupleCursor
import os
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def main_page():
    return render_template('main_page.html')


@app.route('/urls')
def get_urls():
    urls = get_urls_data()

    return render_template(
        'index.html',
        urls=urls,
    )


@app.route('/urls', methods=['POST'])
def post_url():
    user_url = request.form.to_dict()['url']
    normalized_url = normalize(user_url)

    error = validate(normalized_url)
    if error:
        flash(error, 'danger')
        return render_template(
            'main_page.html',
            url=user_url,
        ), 422

    with open_connection() as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
            curs.execute(
                "SELECT * FROM urls WHERE name = %s;",
                (normalized_url,)
            )
            url = curs.fetchone()

        if url:
            url_id = url.id
            flash('Страница уже существует', 'warning')
            return redirect(url_for('get_url', id=url_id))

        with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
            current_date = datetime.now().date()
            curs.execute(
                "INSERT INTO urls (name, created_at) VALUES (%s, %s);",
                (normalized_url, current_date)
            )
            curs.execute(
                "SELECT * FROM urls WHERE name = %s;",
                (normalized_url,)
            )
            url = curs.fetchone()
            url_id = url.id
    flash('Страница успешно добавлена', 'success')
    return redirect(url_for('get_url', id=url_id))


@app.route('/urls/<int:id>')
def get_url(id):
    with open_connection() as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
            curs.execute("SELECT * FROM urls WHERE id = %s;", (id,))
            url = curs.fetchone()
            curs.execute("SELECT * FROM urls_checks\
                WHERE url_id = %s\
                ORDER BY id DESC;", (id,))
            checks = curs.fetchall()

    if not url:
        return render_template(
            'not_found.html',
        ), 404

    return render_template(
        'show.html',
        url=url,
        checks=checks,
    )


@app.route('/urls/<int:id>/checks', methods=['POST'])
def make_check(id):
    with open_connection() as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
            curs.execute("SELECT * FROM urls WHERE id = %s;", (id,))
            url = curs.fetchone()
            url_id = url.id
            url_name = str(url.name)

    try:
        check = requests.get(url_name)
        check.raise_for_status()
    except requests.RequestException:
        flash('Произошла ошибка при проверке', 'danger')
        return redirect(url_for('get_url', id=url_id))
    else:
        status_code = check.status_code
        soup = BeautifulSoup(check.text, 'html.parser')
        h1 = soup.h1.text if soup.h1 else ''
        title = soup.title.text if soup.title else ''
        description_tag = soup.find('meta', attrs={'name': 'description'})
        description = description_tag['content'] if description_tag else ''
        current_date = datetime.now().date()
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
                    (id, status_code, h1, title, description, current_date)
                )
        flash('Страница успешно проверена', 'success')
        return redirect(url_for('get_url', id=url_id))
