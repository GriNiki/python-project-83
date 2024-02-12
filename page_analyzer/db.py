import psycopg2
from psycopg2.extras import DictCursor
import os
from dotenv import load_dotenv
from datetime import date


load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')


def connect_to_db(func):

    def wrapper(*args, **kwargs):

        with psycopg2.connect(DATABASE_URL) as connect_db:
            with connect_db.cursor(cursor_factory=DictCursor) as cur:
                return func(cur, *args, **kwargs)

    return wrapper


@connect_to_db
def add_url(cur, url):
    cur.execute('''
        INSERT INTO urls
        (name, created_at)
        VALUES (%s, %s)
        ''', (url, date.today(),)
    )


@connect_to_db
def get_url_name(cur):
    cur.execute('''
            SELECT name FROM urls
            ''')
    all_urls_name = [url_name[0] for url_name in cur.fetchall()]
    return all_urls_name


@connect_to_db
def get_url_id(cur, name):
    cur.execute('''
            SELECT id FROM urls WHERE name = %s
            ''', (name,)
                )
    row = cur.fetchone()[0]
    return row


@connect_to_db
def get_url_data(cur, url_id):
    cur.execute('''
            SELECT * FROM urls WHERE id = %s
            ''', (url_id,)
                )
    row = cur.fetchone()
    return row


@connect_to_db
def get_all_urls(cur):
    cur.execute('''
            SELECT DISTINCT ON (urls.id)
            urls.id AS id,
            urls.name AS name,
            url_checks.status_code AS status_code,
            url_checks.created_at AS created_at
            FROM urls LEFT JOIN url_checks
            ON urls.id = url_checks.url_id
            ORDER BY urls.id, url_checks.created_at DESC;
            ''')
    row = cur.fetchall()
    return row


@connect_to_db
def add_check_url(cur, url_id, status_code, h1, title, description):
    cur.execute('''
            INSERT INTO url_checks
            (url_id, status_code, h1, title, description, created_at)
            VALUES (%s, %s, %s, %s, %s, %s);
            ''', (url_id, status_code, h1, title, description, date.today(),)
                )


@connect_to_db
def get_url_check(cur, url_id):
    cur.execute('''
            SELECT * FROM url_checks WHERE url_id = %s
            ''', (url_id,)
                )
    row = cur.fetchone()
    return row


@connect_to_db
def truncate_db(curs):
    curs.execute('''
            TRUNCATE urls, url_checks RESTART IDENTITY CASCADE
            ''')
