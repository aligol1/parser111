import base64
import hashlib
import requests
import pprint
from bs4 import BeautifulSoup
from pydantic import BaseModel


HOST = 'https://omr.gov.ua'
URL = 'https://omr.gov.ua/ua/acts/council/'
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.3 Safari/605.1.15'
}
class Document(BaseModel):
    title: str
    link: str
    file_content: str
    file_name: str


def get_html(url, params=None) -> requests.Response:
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('td', class_='col-3')
    href_list = []
    for td in items:
        td:BeautifulSoup
        if td.find('a'):
            href_list.append(HOST + td.a.attrs.get('href'))

def rishennya(url:str)-> Document:
    page = get_html(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    if soup.find('h1'):
        title = soup.find('h1').text
    else:
        title = 'Заголовок не найден'
    if soup.find('article'):
        text = soup.find('article').text
    else:
        text = 'Текст не найден'
    hash_object = hashlib.md5(text.encode())
    md5_hash = hash_object.hexdigest()

    return Document.parse_obj({
        'title':title,
        'link':url,
        'file_content':base64.b64encode(text.encode()).decode(),
        'file_name': md5_hash+'.txt'
    })


def parse():
    html = get_html(URL)
    if html.status_code == 200:
        get_content(html.text)
    else:
        print('Error')


if __name__ == '__main__':
    a=rishennya('https://omr.gov.ua/ua/acts/council/183703/')
    pprint.pprint(a)

