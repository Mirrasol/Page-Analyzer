from validators import url as validate_url


def validate(url):
    if not validate_url(url):
        return 'Некорректный URL'
    elif len(url) > 255:
        return 'URL превышает 255 символов'
