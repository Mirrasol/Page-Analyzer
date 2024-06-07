from urllib.parse import urlparse


def normalize(url):
    parse_result = urlparse(url)
    return f'{parse_result.scheme}://{parse_result.netloc}'
