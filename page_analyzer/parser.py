from bs4 import BeautifulSoup
from datetime import datetime


def parse_check(check):
    check_data = check.text
    soup = BeautifulSoup(check_data, 'html.parser')
    status_code = check.status_code
    h1 = soup.h1.text if soup.h1 else ''
    title = soup.title.text if soup.title else ''
    description_tag = soup.find('meta', attrs={'name': 'description'})
    description = description_tag['content'] if description_tag else ''
    current_date = datetime.now().date()
    return status_code, h1, title, description, current_date
