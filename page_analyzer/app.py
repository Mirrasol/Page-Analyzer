from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from page_analyzer.validator import validate
from page_analyzer.normalizer import normalize
from page_analyzer.db_logic import open_connection
from psycopg2.extras import NamedTupleCursor
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def main_page():
    return render_template('main_page.html')


@app.route('/urls')
def get_urls():
    with open_connection() as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
            curs.execute("SELECT * FROM urls ORDER BY id DESC;")
            urls = curs.fetchall()

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
            current_date = datetime.now().date()
            curs.execute(
                "INSERT INTO urls_checks (url_id, description, created_at)\
                VALUES (%s, %s, %s);",
                (id, None, current_date)
            )
            curs.execute(
                "SELECT * FROM urls WHERE id = %s;",
                (id,)
            )
            url = curs.fetchone()
            url_id = url.id
        flash('Страница успешно проверена', 'success')
        return redirect(url_for('get_url', id=url_id))
