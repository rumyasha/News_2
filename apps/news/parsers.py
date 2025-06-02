import aiohttp
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Dict, Optional


class KaktusMediaParser:
    BASE_URL = "https://kaktus.media"

    async def parse_articles(self, html: str) -> List[Dict]:
        """Парсинг списка статей из HTML"""
        soup = BeautifulSoup(html, 'lxml')
        articles = []

        for item in soup.select('.Tag--article'):
            try:
                title = item.select_one('.ArticleItem--name').text.strip()
                url = item.select_one('.ArticleItem--name')['href']
                time = item.select_one('.ArticleItem--time').text.strip()

                articles.append({
                    'title': title,
                    'url': url,
                    'time': time,
                    'source': 'Kaktus Media'
                })
            except Exception as e:
                print(f"Ошибка парсинга статьи: {e}")
                continue

        return articles

    async def fetch_news(self, date: datetime) -> Dict:
        """Получение новостей за указанную дату"""
        date_str = date.strftime("%Y-%m-%d")
        url = f"{self.BASE_URL}/?lable=8&date={date_str}&order=time"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    html = await response.text()
                    return {
                        'date': date_str,
                        'articles': await self.parse_articles(html),
                        'source': self.BASE_URL
                    }
                return {'date': date_str, 'articles': []}