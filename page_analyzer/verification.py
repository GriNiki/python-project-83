import validators
from urllib.parse import urlparse


def validate(url):

    if 255 >= len(url) > 0 and validators.url(url):
        return f"{urlparse(url).scheme}://{urlparse(url).hostname}"

    else:
        return False
