import aiohttp
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from typing import List, Dict, Union, Optional

class KaktusMediaParser:
    """Асинхронный парсер новостей с Kaktus Media"""

    BASE_URL = "https://kaktus.media"

    def __init__(self):
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def _fetch_html(self, url: str) -> Optional[str]:
        """Асинхронно получает HTML страницы"""
        try:
            async with self.session.get(url) as response:
                if response.status == 200:
                    return await response.text()
                print(f"Ошибка запроса: {response.status}")
                return None
        except Exception as e:
            print(f"Ошибка при запросе {url}: {e}")
            return None

    async def _parse_articles(self, html: str) -> List[Dict[str, str]]:
        """Парсит список статей из HTML"""
        soup = BeautifulSoup(html, 'lxml')
        sections = soup.find_all('div', class_="Tag--articles")
        news_list = []

        for tag in sections:
            articles = tag.find_all('div', class_="Tag--article")
            for article in articles:
                try:
                    title_elem = article.find('a', class_='ArticleItem--name')
                    time_elem = article.find('div', class_='ArticleItem--time')

                    if not title_elem or not time_elem:
                        continue

                    news_list.append({
                        'time': time_elem.text.strip(),
                        'title': title_elem.text.strip(),
                        'url': title_elem['href'],
                        'source': 'Kaktus Media'
                    })
                except Exception as e:
                    print(f"Ошибка парсинга статьи: {e}")

        return news_list

    async def get_news_by_date(self, date: Union[datetime, str]) -> Dict:
        """Получает новости для указанной даты"""
        if isinstance(date, datetime):
            date_str = date.strftime("%Y-%m-%d")
        else:
            date_str = date

        url = f"{self.BASE_URL}/?lable=8&date={date_str}&order=time"
        html = await self._fetch_html(url)

        if not html:
            return {
                'error': 'Failed to fetch page',
                'date': date_str,
                'articles': []
            }

        articles = await self._parse_articles(html)
        date_title = await self._parse_date(html)

        return {
            'date': date_title or date_str,
            'articles': articles,
            'source': self.BASE_URL,
            'retrieved_at': datetime.now().isoformat()
        }

    async def _parse_date(self, html: str) -> Optional[str]:
        """Извлекает дату из HTML страницы"""
        soup = BeautifulSoup(html, 'lxml')
        date_element = soup.find('span', class_='PaginatorDate--today-text')
        return date_element.text.replace('  ', '').strip() if date_element else None

    async def get_today_news(self) -> Dict:
        """Новости за сегодня"""
        today = datetime.now()
        return await self.get_news_by_date(today)

    async def get_yesterday_news(self) -> Dict:
        """Новости за вчера"""
        yesterday = datetime.now() - timedelta(days=1)
        return await self.get_news_by_date(yesterday)

    async def get_last_two_days_news(self) -> Dict:
        """Новости за последние 2 дня (сегодня + вчера)"""
        today = await self.get_today_news()
        yesterday = await self.get_yesterday_news()

        return {
            'period': 'last_two_days',
            'total_articles': len(today['articles']) + len(yesterday['articles']),
            'days': {
                'today': today,
                'yesterday': yesterday
            }
        }


import asyncio

async def example_usage():
    async with KaktusMediaParser() as parser:
        # Получаем сегодняшние новости
        today_news = await parser.get_today_news()
        print(f"Сегодня ({today_news['date']}): {len(today_news['articles'])} новостей")

        yesterday_news = await parser.get_yesterday_news()
        print(f"Вчера ({yesterday_news['date']}): {len(yesterday_news['articles'])} новостей")

        last_two_days = await parser.get_last_two_days_news()
        print(f"Всего за 2 дня: {last_two_days['total_articles']} новостей")

if __name__ == "__main__":
    asyncio.run(example_usage())
