import psycopg2
from psycopg2.extras import DictCursor
import os
from dotenv import load_dotenv
from datetime import date


load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')


def add_url(url):

    with psycopg2.connect(DATABASE_URL) as connect_db:
        with connect_db.cursor() as cur:
            cur.execute('''
                    INSERT INTO urls
                    (name, created_at)
                    VALUES (%s, %s)
                    ''', (url, date.today(),)
                        )


def get_url_name():

    with psycopg2.connect(DATABASE_URL) as connect_db:
        with connect_db.cursor() as cur:
            cur.execute('''
                    SELECT name FROM urls
                    ''')
            all_urls_name = [url_name[0] for url_name in cur.fetchall()]

        return all_urls_name


def get_url_id(name):

    with psycopg2.connect(DATABASE_URL) as connect_db:
        with connect_db.cursor() as cur:
            cur.execute('''
                    SELECT id FROM urls WHERE name = %s
                    ''', (name,)
                        )
            row = cur.fetchone()[0]

        return row


def get_url_data(url_id):

    with psycopg2.connect(DATABASE_URL) as connect_db:
        with connect_db.cursor(cursor_factory=DictCursor) as cur:
            cur.execute('''
                    SELECT * FROM urls WHERE id = %s
                    ''', (url_id,)
                        )
            row = cur.fetchone()

        return row


def get_all_urls():

    with psycopg2.connect(DATABASE_URL) as connect_db:
        with connect_db.cursor(cursor_factory=DictCursor) as cur:
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


def add_check_url(url_id, status_code, h1, title, description):

    with psycopg2.connect(DATABASE_URL) as connect_db:
        with connect_db.cursor() as cur:
            cur.execute('''
                    INSERT INTO url_checks
                    (url_id, status_code, h1, title, description, created_at)
                    VALUES (%s, %s, %s, %s, %s, %s);
                    ''', (url_id, status_code, h1, title, description, date.today(),)
                        )


def get_url_check(url_id):

    with psycopg2.connect(DATABASE_URL) as connect_db:
        with connect_db.cursor(cursor_factory=DictCursor) as cur:
            cur.execute('''
                    SELECT * FROM url_checks WHERE url_id = %s
                    ''', (url_id,)
                        )
            row = cur.fetchone()

        return row
