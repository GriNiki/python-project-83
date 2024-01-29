from flask import (
    Flask,
    render_template,
    request,
    flash,
    get_flashed_messages,
    url_for,
    redirect
)
import page_analyzer.db as db
from page_analyzer.verification import validate
import os


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
        )

    validate_url = validate(url)
    urls = db.get_url_name()

    if validate_url in urls:
        flash('URL уже добавлен', 'warning')

    else:
        db.add_url(validate_url)
        flash('URL успешно добавлен', 'success')
    url_id = db.get_url_id(validate_url)
    return redirect(url_for('url_page', id=url_id))


@app.get('/urls')
def get_urls():

    all_urls = db.get_all_urls()

    return render_template('urls.html', urls=all_urls)


@app.route('/urls/<int:id>')
def url_page(url_id):

    url_info = db.get_url_data(url_id)
    massage = get_flashed_messages(with_categories=True)

    if not url_info:
        return render_template('errors/404.html'), 404

    return render_template('page.html', massage=massage,
                           url=url_info)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if __name__ == '__main__':
    app.run()
