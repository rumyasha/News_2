import requests
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urljoin
import time
import json


class PureNewsParser:
    """
    Чистый парсер новостей без использования БД.
    Все данные хранятся только в оперативной памяти.
    """

    def __init__(self):
        self.news_data = {
            'sources': {},
            'last_update': None,
            'total_articles': 0
        }
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

    def parse_site(self, url):
        """Основной метод парсинга сайта"""
        try:
            print(f"Парсим {url}...")
            response = self.session.get(url)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            articles = self._find_articles(soup)

            parsed_articles = []
            for item in articles:
                article = self._parse_article(item, url)
                if article:
                    parsed_articles.append(article)

            self.news_data['sources'][url] = {
                'last_parsed': datetime.now().isoformat(),
                'articles': parsed_articles,
                'count': len(parsed_articles)
            }
            self.news_data['total_articles'] += len(parsed_articles)
            self.news_data['last_update'] = datetime.now().isoformat()

            return True

        except Exception as e:
            print(f"Ошибка при парсинге {url}: {str(e)}")
            return False

    def _find_articles(self, soup):
        """Поиск новостных блоков на странице"""
        # Универсальные селекторы для разных сайтов
        selectors = [
            {'name': 'article', 'class_': 'news-item'},
            {'name': 'div', 'class_': 'article'},
            {'name': 'li', 'class_': 'post'},
            {'name': 'article', 'class_': None}
        ]

        for selector in selectors:
            articles = soup.find_all(selector['name'], class_=selector['class_'])
            if articles:
                return articles
        return []

    def _parse_article(self, item, base_url):
        """Парсинг отдельной новости"""
        try:
            # Заголовок
            title_elem = item.find(['h1', 'h2', 'h3', 'h4']) or item.find('a', class_='title')
            title = title_elem.get_text(strip=True) if title_elem else 'Без названия'

            # Ссылка
            link = item.find('a')
            url = urljoin(base_url, link['href']) if link and 'href' in link.attrs else None

            # Контент
            content_elem = item.find(['div', 'p'], class_=['content', 'text', None])
            content = content_elem.get_text(strip=True) if content_elem else ''

            # Дата
            date_elem = item.find('time') or item.find('span', class_='date')
            date = date_elem['datetime'] if date_elem and 'datetime' in date_elem.attrs else (
                date_elem.get_text(strip=True) if date_elem else datetime.now().isoformat()
            )

            # Изображение
            img = item.find('img')
            image = urljoin(base_url, img['src']) if img and 'src' in img.attrs else None

            return {
                'title': title,
                'url': url,
                'content': content[:500] + '...' if len(content) > 500 else content,  # Обрезаем длинный текст
                'date': date,
                'image': image,
                'source': base_url
            }

        except Exception as e:
            print(f"Ошибка парсинга статьи: {str(e)}")
            return None

    def save_to_json(self, filename='news.json'):
        """Сохранение данных в JSON файл"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.news_data, f, ensure_ascii=False, indent=2)
        print(f"Данные сохранены в {filename}")

    def parse_multiple(self, urls, delay=2):
        """Парсинг нескольких сайтов"""
        for url in urls:
            self.parse_site(url)
            time.sleep(delay)  # Задержка между запросами


# Пример использования
if __name__ == "__main__":
    parser = PureNewsParser()

    # Список новостных сайтов для парсинга
    news_sites = [
        'https://ria.ru',
        'https://lenta.ru',
        'https://www.kommersant.ru'
    ]

    # Запуск парсинга
    parser.parse_multiple(news_sites)

    # Сохранение результатов
    parser.save_to_json()

    # Вывод статистики
    print(f"\nВсего спаршено {parser.news_data['total_articles']} статей")
    for url, data in parser.news_data['sources'].items():
        print(f"{url}: {data['count']} статей")