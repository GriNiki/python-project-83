import pytest
from page_analyzer import app
from page_analyzer.verification import validate
from page_analyzer.db import truncate_db


class TestApp:

    def setup(self):

        app.testing = True
        self.client = app.test_client()

    def test_main(self):

        response = self.client.get('/')
        data = response.data.decode('utf-8')
        assert response.status_code == 200
        assert 'Анализатор страниц' in data

    def test_get_urls(self):

        response = self.client.get('/urls')
        data = response.data.decode('utf-8')
        assert response.status_code == 200
        assert 'Сайты' in data

    @pytest.mark.parametrize('url, flashed_message',
                             [('https://ru.hexlet.io/projects/83/members/35932/reviews', 'Страница успешно добавлена'),
                              ('wrong://www.wrong.wrong', 'Некорректный URL'),
                              ],)
    def test_post_urls(self, url, flashed_message):

        response = self.client.post('/urls', data={'url': url})
        data = response.data.decode('utf-8')

        if validate(url):

            if flashed_message == 'Страница уже существует':
                assert response.status_code == 302
                response = self.client.get('/urls/1')
                data = response.data.decode('utf-8')
                assert flashed_message in data

            else:
                assert validate(url) == 'https://ru.hexlet.io'
                assert response.status_code == 302
                response = self.client.get('/urls/1')
                data = response.data.decode('utf-8')
                assert flashed_message in data

        else:
            assert not validate(url)
            assert response.status_code == 422
            assert flashed_message in data

    @pytest.mark.parametrize('url, flashed_message',
                             [('https://ru.hexlet.io/projects/83/members/35932/reviews', 'Страница успешно проверена'),
                              ('https://www.wrong.ru', 'Произошла ошибка при проверке'),
                              ], )
    def test_check_url(self, url, flashed_message):

        self.client.post('/urls', data={'url': url})
        response = self.client.post('/urls/1/checks')

        if url == 'https://www.wrong.ru':
            assert response.status_code == 302
            response = self.client.get('/urls/1')
            data = response.data.decode('utf-8')
            assert flashed_message in data

        else:
            assert response.status_code == 302
            response = self.client.get('/urls/1')
            data = response.data.decode('utf-8')
            assert flashed_message in data
            assert '200' in data
            assert 'Лучшая школа программирования' in data
            assert 'Хекслет — онлайн-школа программирования, онлайн-обучение ИТ-профессиям' in data
            assert 'Авторские программы обучения с практикой и готовыми проектами в резюме.' in data

    def teardown(self):
        truncate_db()
        pass
