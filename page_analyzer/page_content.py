from bs4 import BeautifulSoup


def get_content(data):

    soup = BeautifulSoup(data.text, 'html.parser')

    if soup.h1:
        h1 = soup.h1.get_text()

    else:
        h1 = ''

    if soup.title:
        title = soup.title.get_text()

    else:
        title = ''

    if soup.find('meta', {'name': 'description'}):
        description = soup.find('meta', {'name': 'description'}).get('content')

    else:
        description = ''

    return h1, title, description
