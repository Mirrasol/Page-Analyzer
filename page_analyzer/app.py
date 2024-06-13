from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from page_analyzer.db_manager import (
    get_urls_data,
    get_url_data,
    get_url_checks,
    get_url_id,
    post_new_url,
    post_new_check,
)
from page_analyzer.normalizer import normalize
from page_analyzer.validator import validate
from page_analyzer.parser import parse_check
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

    url_id = get_url_id(normalized_url)
    if url_id:
        flash('Страница уже существует', 'warning')
        return redirect(url_for('get_url', id=url_id))
    else:
        post_new_url(normalized_url)
        url_id = get_url_id(normalized_url)
        flash('Страница успешно добавлена', 'success')
        return redirect(url_for('get_url', id=url_id))


@app.route('/urls/<int:id>')
def get_url(id):
    url = get_url_data(id)
    checks = get_url_checks(id)

    if not url:
        return render_template(
            'not_found.html',
        ), 404

    return render_template(
        'show_url.html',
        url=url,
        checks=checks,
    )


@app.route('/urls/<int:id>/checks', methods=['POST'])
def make_check(id):
    url = get_url_data(id)
    url_name = url.name

    try:
        check = requests.get(url_name)
        check.raise_for_status()
    except requests.RequestException:
        flash('Произошла ошибка при проверке', 'danger')
        return redirect(url_for('get_url', id=id))
    else:
        status_code, h1, title, description, current_date = parse_check(check)
        post_new_check(id, status_code, h1, title, description, current_date)
        flash('Страница успешно проверена', 'success')
        return redirect(url_for('get_url', id=id))
