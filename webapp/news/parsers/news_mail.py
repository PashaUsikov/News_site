from bs4 import BeautifulSoup
from flask import current_app
from datetime import datetime
from webapp.db import db
from webapp.news.models import News
from webapp.news.parsers.utils import get_html, save_news

# Получаем страницу новостей
def get_news(html):
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        all_news = soup.find('div', class_='d6050750fd').findAll('div', class_='ae54c73111')
        return all_news
    return False


# Форматируем дату публикаций
def date_of_publication(published):
    date_string = ''
    for date_ in str(published).split()[2]:
        if date_ in '0123456789-':
            date_string += date_
        if date_ == 'T':
            break       
    try:
        return datetime.strptime(date_string, '%Y-%m-%d')
    except ValueError:
        return datetime.now()


# Определяем заголовки статей и сохраняем в БД
def get_news_snippets():
    html = get_html(current_app.config["DATASET_URL"])
    for news in get_news(html):
        title = news.find('div', class_='d046a5563e').find('a').text
        url = news.find('div', class_='d046a5563e').find('a')['href']
        published = news.find('time')
        published = date_of_publication(published)
        picture = news.find('div', class_='cbe01067c6').find('img')['src']
        save_news(title, url, published, picture)


# Выбираем новости из БД без текста
def get_news_content():
    news_without_text = News.query.filter(News.text.is_(None))
    return news_without_text


# Получаем содержимое каждой статьи в HTML
def get_news_article():
    for news in get_news_content():
        html = get_html(news.url)
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            try:
                part1 = soup.find('header', class_='c91838a669').find('time').decode_contents()
            except AttributeError:
                part1 = soup.find('span', class_='note__text breadcrumbs__text js-ago').decode_contents()
            try:
                part2 = soup.find('header', class_='c91838a669').\
            find('div', class_='cca994f104 f8ce0d2d79 c6d5585012').decode_contents()
            except AttributeError:
                part2 = soup.find('div', class_='article__intro').decode_contents()
            try:
                part3 = soup.find('main', itemprop="articleBody").decode_contents()
            except AttributeError:
                part3 = soup.find('div', class_=
                "article__text js-module js-view js-media-stat-article js-smoky-links").decode_contents()
        return part1 + part2 + part3
           

# Сохраняем содержимое каждой статьи в БД
def save_news_article():
    for news in get_news_content():
        article = get_news_article()
        if article:
            news.text = article
            db.session.add(news)
            db.session.commit()