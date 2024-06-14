from validators import url as validate_url


def validate(url):
    """Check that the given address is a valid URL."""
    if not validate_url(url):
        return 'Некорректный URL'
    elif len(url) > 255:
        return 'URL превышает 255 символов'
