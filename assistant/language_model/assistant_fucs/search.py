from bs4 import BeautifulSoup
import requests


def search():

    url = 'http://yandex.ru/yandsearch?text=%(q)s'
    payload = {'q': 'Python', }
    r = requests.get(url % payload)
    print(r.text)
    # breakpoint()
    soup = BeautifulSoup(r.text, features="html.parser")
    titles = [item.text for item in soup.findAll('div', attrs={'class': 'b-serp-item__text'})]
    for t in titles:
        print(t)


if __name__ == '__main__':
    search()

