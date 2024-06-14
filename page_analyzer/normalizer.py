from urllib.parse import urlparse


def normalize(url):
    """Return the given URL address in the specified format."""
    parse_result = urlparse(url)
    return f'{parse_result.scheme}://{parse_result.netloc}'
