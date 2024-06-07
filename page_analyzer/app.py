from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from dotenv import load_dotenv
from validator import validate
from normalizer import normalize
import psycopg2
import os

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
conn = psycopg2.connect(DATABASE_URL)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def main_page():
    return render_template('main_page.html')


@app.route('/urls')
def get_urls():
    urls = PLACEHOLDER_get_database()
    return render_template(
        'index.html',
        urls=urls,
    )


@app.route('/urls', methods=['POST'])
def post_url():
    urls = PLACEHOLDER_get_database()
    user_url = request.form.get('url')
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

    urls.PLACEHOLDER_save(normalized_url)
    flash('Страница успешно добавлена', 'success')
    return redirect(url_for('get_url', id=url_id))


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
