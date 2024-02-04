from flask import (
    Flask,
    render_template,
    request,
    flash,
    get_flashed_messages,
    url_for,
    redirect
)
import requests
from requests import ConnectionError, HTTPError
import page_analyzer.db as db
from page_analyzer.verification import validate
import os
from page_analyzer.page_content import get_content
from dotenv import load_dotenv


load_dotenv()


app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')


@app.route("/")
def get_main():

    messages = get_flashed_messages(with_categories=True)

    return render_template("index.html", url='', messages=messages)


@app.post("/urls")
def post_urls():

    url = request.form.get('url')

    if not validate(url):
        flash("Некорректный URL", 'warning')
        return render_template(
            'index.html',
            url=url,
            messages=get_flashed_messages(with_categories=True)
        ), 422

    validate_url = validate(url)
    urls = db.get_url_name()

    if validate_url in urls:
        flash('Страница уже существует', 'warning')

    else:
        db.add_url(validate_url)
        flash('Страница успешно добавлена', 'success')

    url_id = db.get_url_id(validate_url)

    return redirect(url_for('url_page', id=url_id))


@app.get('/urls')
def get_urls():

    all_urls = db.get_all_urls()

    return render_template('urls.html', urls=all_urls)


@app.route('/urls/<int:id>')
def url_page(id):

    url_info = db.get_url_data(id)
    url_check = db.get_url_check(id)
    massage = get_flashed_messages(with_categories=True)

    if not url_info:
        return render_template('errors/404.html'), 404

    return render_template('page.html', massage=massage,
                           url=url_info, check=url_check)


@app.post('/urls/<int:id>/checks')
def check_url(id):

    url_name = db.get_url_data(id).get('name')
    url_id = db.get_url_data(id).get('id')

    try:
        req = requests.get(url_name)
        req.raise_for_status()

    except (ConnectionError, HTTPError):
        flash('Произошла ошибка при проверке', 'warning')
        return redirect(url_for('url_page', id=url_id))

    h1, title, description = get_content(req)
    status = req.status_code
    db.add_check_url(url_id, status, h1, title, description)
    flash('Страница успешно проверена', 'success')

    return redirect(url_for('url_page', id=url_id))


@app.errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if __name__ == '__main__':
    app.run()
