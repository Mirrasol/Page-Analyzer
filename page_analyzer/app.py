from flask import (
    Flask,
    flash,
    get_flashed_messages,
    redirect,
    render_template,
    request,
    url_for,
)
from dotenv import load_dotenv
import psycopg2
import os

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
conn = psycopg2.connect(DATABASE_URL)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def main_page():
    messages = get_flashed_messages(with_categories=True)
    return render_template(
        'main_page.html',
        messages=messages,
    )


@app.route('/urls')
def get_urls():
    urls = PLACEHOLDER_get_database()
    messages = get_flashed_messages(with_categories=True)
    return render_template(
        'index.html',
        urls=urls,
        messages=messages,
    )


@app.route('/urls', methods=['POST'])
def post_url():
    urls = PLACEHOLDER_get_database()
    url = request.form.to_dict()
    errors = PLACEHOLDER_validate(url)

    if errors:
        return render_template(
            'main_page.html',
            url=url,
            errors=errors
        ), 422

    urls.PLACEHOLDER_save(url)
    flash('Страница успешно добавлена', 'success')
    return redirect(url_for('get_url(id)'), code=302)


@app.route('/urls/<int:id>')
def get_url(id):
    urls = PLACEHOLDER_get_database()
    url = urls.PLACEHOLDER_find(id)

    if not url:
        return 'Page not found', 404

    return render_template(
        'show.html',
        url=url,
    )
