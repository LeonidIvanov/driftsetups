from bs4 import BeautifulSoup
from urllib.request import urlopen
from time import sleep
from random import randint


start_url = 'http://www.drom.ru/catalog/'
parsed_urls = ['/catalog/~search/',]
engines = []


def parser(url):
    start_url_resp = urlopen(url)
    soup = BeautifulSoup(start_url_resp, 'html.parser')
    brand_list = soup.find_all('div', {'class': 'b-selectCars__section'})
    print(brand_list)
    brand_url_list = [a['href'] for a in brand_list[-1].find_all('a', href=True)]
    engines_by_brand = ['http://www.drom.ru{}engine/'.format(url) for url in brand_url_list]
    for url in engines_by_brand:
        url_resp = urlopen(url)
        soup = BeautifulSoup(url_resp, 'html.parser')
        brand_name = soup.h1.getText().split('Двигатели ')[1:][0]
        div = soup.find('div', {'data-print': 'advert'})
        with open('engines.txt', 'a') as file:
            for a in div.find_all('a', href=True):
                if a.getText():
                    engine = '{0};{1}'.format(brand_name, a.getText())
                    if engine not in engines:
                        engines.append(engine)
                        print(engine)
                        file.write(engine + '\n')
        file.close()


def wiki_h3_scraper(url):
    resp = urlopen(url)
    soup = BeautifulSoup(resp, 'html.parser')
    h3s = soup.find_all('h3')
    with open('engines.txt', 'a') as file:
        for h3 in h3s:
            engine = 'Toyota;{}'.format(h3.getText())
            print(engine)
            file.write(engine + '\n')
    file.close()


def uniqueify():
    with open('engines.txt', 'r') as file:
        engines_set = list(set(file.readlines()))
        print(sorted(engines_set))
        with open('cleared_engines.txt', 'w') as engines_file:
            for engine in sorted(engines_set):
                engines_file.write(engine)
        engines_file.close()
    file.close()


def doubled_engines():
    with open('cleared_engines.txt', 'r') as file:
        engines = sorted(set(file.readlines()))
        for engine in enumerate(engines):
            for compared_engine in engines[engine[0]+1:-1]:
                if engine[1].split(';')[1] == compared_engine.split(';')[1]:
                    print(engine)
# def parser(url):
#     start_url_resp = urlopen(url)
#     soup = BeautifulSoup(start_url_resp, 'html.parser')
#     urls_from_page = []
#     for a in soup.find_all('a', href=True):
#         if '/catalog/' in a['href'] and '#' not in a['href']:
#             if 'http://www.drom.ru' not in a['href']:
#                 a['href'] = 'http://www.drom.ru{}'.format(a['href'])
#             urls_from_page.append(a['href'])
#     for url in urls_from_page:
#         if url not in parsed_urls:
#             print(url)
#             sleep(randint(2, 6))
#             parsed_urls.append(url)
#             html = urlopen(url)
#             soup = BeautifulSoup(html, 'html.parser')
#             h1 = soup.find('h1').text()
#             print(h1)
#             if h1 and 'Двигатель' in h1:
#                 engine_model = h1.split(' ')[1:]
#                 print(engine_model)
#                 with open('engines.txt', 'a') as file:
#                     file.write(engine_model + '\n')
#                     file.close()
#             for a in soup.find_all('a', href=True):
#                 if '/catalog/' in a['href'] and '#' not in a['href'] and a['href'] not in parsed_urls:
#                     if 'http://www.drom.ru' not in a['href']:
#                         a['href'] = 'http://www.drom.ru{}'.format(a['href'])
#                     urls_from_page.append(a['href'])
#             urls_from_page.remove(url)
#         else:
#             print('Already parsed')
#     print('Finished!')



if __name__ == '__main__':
    # parser(start_url)
    # wiki_h3_scraper('https://en.wikipedia.org/wiki/Toyota_A_engine')
    uniqueify()
    doubled_engines()
