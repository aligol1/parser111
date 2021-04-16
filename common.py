import base64
import hashlib
import os

import requests
from bs4 import BeautifulSoup
from pydantic.main import BaseModel

from cfg import HEADERS, HOST, URL, FILE_BASE, LNK, KEY

class Document(BaseModel):
    '''Структура описывающая формат принемаемый API'''
    title: str
    link: str
    file_content: str
    file_name: str


def get_html(url, params=None) -> requests.Response:
    '''Получить содержимое страницы'''
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_content(html: str) -> list[str]:
    ''' Получить список ссылок на документы из страницы '''
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('td', class_='col-3')
    href_list = []
    for td in items:

        td: BeautifulSoup
        if td.find('a'):
            href_list.append(HOST + td.a.attrs.get('href'))
    return href_list


def rishennya(url: str = '') -> Document:
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
        'title': title,
        'link': url,
        'file_content': base64.b64encode(text.encode()).decode(),
        'file_name': md5_hash + '.txt'
    })


def get_list_rishen() -> list[str]:
    html = get_html(URL)
    if html.status_code == 200:
        return get_content(html.text)

    else:
        print('Error')


def load_visited_links() -> list[str]:
    '''Загружаем лист обработанных ссылок'''
    poseshennyi = []
    if os.path.exists(FILE_BASE):
        with open(FILE_BASE) as fp:
            temp = fp.readlines()
            for i in temp:
                poseshennyi.append(i.strip())
    return poseshennyi


def store_link(doc: Document):
    '''Добавляем посещенную ссылку в file.db'''
    with open(FILE_BASE, "a") as fp:
        fp.write(doc.link + "\n")


def send_to_check(doc: Document):
    '''Отправляет документ по API на проверку'''
    response = requests.post(LNK,
                             json=doc.dict(),
                             headers={'AUTHORIZATION': KEY})
    return response
