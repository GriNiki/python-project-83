import psycopg2
from psycopg2.extras import DictCursor
import os
from dotenv import load_dotenv
from datetime import datetime


load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')


def add_url(url):

    connect_db = psycopg2.connect(DATABASE_URL)

    with connect_db.cursor() as cur:
        cur.execute('''INSERT INTO urls
                    (name, created_at)
                    VALUES (%s, %s)''', (url, datetime.now(),))
        connect_db.commit()
    connect_db.close()


def get_url_name():

    connect_db = psycopg2.connect(DATABASE_URL)

    with connect_db.cursor() as cur:
        cur.execute("SELECT name FROM urls")
        all_urls_name = [url_name[0] for url_name in cur.fetchall()]
        return all_urls_name


def get_url_id(name):

    connect_db = psycopg2.connect(DATABASE_URL)

    with connect_db.cursor() as cur:
        cur.execute("SELECT id FROM urls WHERE name = %s", (name,))
        row = cur.fetchone()[0]
    return row


def get_url_data(url_id):

    connect_db = psycopg2.connect(DATABASE_URL)

    with connect_db.cursor(cursor_factory=DictCursor) as cur:
        cur.execute("SELECT * FROM urls WHERE id = %s", (url_id,))
        row = cur.fetchone()
    return row


def get_all_urls():

    connect_db = psycopg2.connect(DATABASE_URL)

    with connect_db.cursor(cursor_factory=DictCursor) as cur:
        cur.execute("""
                SELECT DISTINCT ON (urls.id)
                urls.id AS id,
                urls.name AS name
                FROM urls ORDER BY urls.id DESC;
                """)
        row = cur.fetchall()
    return row


# def check_url(url):
#     connect_db = connect(DATABASE_URL)
#
#     with connect_db.cursor(coursor_factory = psycopg2.extras.DictCursor) as curs:
#         curs.execute('''SELECT * FROM urls
#                     WHERE name=%s''', (url,))
#         record_url = curs.fetchone()
#
#     if record_url:
#         return True
