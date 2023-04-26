import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

URL = "https://vesti-kalmykia.ru/news"


def get_links(URL):
    s = requests.session()
    links_list = []
    count = 0
    for i in range(1,69):
        response = s.get(url=f'{URL}/{i}')
        soup = bs(response.text, 'lxml')
        news_links = soup.find_all("div", class_="teaser-item post")
        for item in news_links:
            link = URL + item.find("a", class_="item-link").get("href")[5:]
            print(link)
            links_list.append(link)
            count += 1
            if count < 999:
                continue
            else:
                break
    return links_list


def get_titles(response):
    soup = bs(response.text, 'lxml')
    title = soup.find("h1", class_="item-title uk-margin")
    return title.text.strip()


def get_text(response):
    soup = bs(response.text, 'lxml')
    text = soup.find("div", class_="item-text uk-margin")
    if text == None:
        text = soup.find("h1", class_="item-title uk-margin")
        return str(text)
    return text.text.strip()


def get_date(response):
    soup = bs(response.text, 'lxml')
    date = soup.find("div", class_="uk-width-expand@m").find("div", class_="item-date")
    return date.text.strip()


def main():
    links = get_links(URL)
    titles = []
    texts = []
    dates = []
    for link in links:
        response = requests.get(link)  # делаю запрос по ссылке

        text = get_text(response)  # получаю текст по запросу

        title = get_titles(response)  # получаю заголовок новости

        date = get_date(response)  # получаю дату публикации

        texts.append(text)  # добавляю текст новости

        titles.append(title)  # добавляю заголовок новости

        dates.append(date)  # добавляю дату публикации
    data = {'URL': links, 'TITLE': titles, 'TEXT': texts, 'DATE': dates}
    df = pd.DataFrame(data)
    df.to_csv('df.csv')


if __name__ == '__main__':
    main()
