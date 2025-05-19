# news/views.py
from django.http import JsonResponse
from django.views import View
from django.core.cache import cache
from datetime import datetime, timedelta
import aiohttp
from bs4 import BeautifulSoup
import asyncio


class KaktusNewsMixin:
    """Общие методы для работы с Kaktus Media"""

    @staticmethod
    async def _parse_articles(html):
        """Парсинг статей из HTML"""
        soup = BeautifulSoup(html, 'lxml')
        sections = soup.find_all('div', class_="Tag--articles")
        news_list = []

        for tag in sections:
            tags = tag.find_all('div', class_="Tag--article")
            for i in tags:
                try:
                    site = i.find('a', class_='ArticleItem--name')['href']
                    title = i.find('a', class_='ArticleItem--name').text.strip()
                    time = i.find('div', class_='ArticleItem--time').text.strip()
                    news_list.append({
                        'time': time,
                        'title': title,
                        'url': site
                    })
                except Exception as e:
                    print(f"Error extracting article data: {e}")

        return news_list


class TodayNewsView(View, KaktusNewsMixin):
    """Новости за сегодня"""

    async def get(self, request):
        cache_key = 'kaktus_today_news'
        cached_data = cache.get(cache_key)

        if cached_data:
            return JsonResponse(cached_data)

        current_date = datetime.now().strftime("%Y-%m-%d")
        url = f'https://kaktus.media/?lable=8&date={current_date}&order=time'

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        html = await response.text()
                        articles = await self._parse_articles(html)

                        # Получаем дату
                        date = await self._get_date(html)

                        result = {
                            'date': date,
                            'articles': articles,
                            'source': 'kaktus.media',
                            'last_updated': datetime.now().isoformat()
                        }

                        # Кэшируем на 10 минут
                        cache.set(cache_key, result, timeout=600)
                        return JsonResponse(result)
                    else:
                        return JsonResponse(
                            {'error': 'Failed to fetch news', 'status': response.status},
                            status=500
                        )
        except Exception as e:
            return JsonResponse(
                {'error': str(e), 'type': 'connection_error'},
                status=500
            )

    async def _get_date(self, html):
        soup = BeautifulSoup(html, 'lxml')
        date_element = soup.find('span', class_='PaginatorDate--today-text')
        return date_element.text.replace('  ', '') if date_element else datetime.now().strftime("%d.%m.%Y")


class YesterdayNewsView(View, KaktusNewsMixin):
    """Новости за вчера"""

    async def get(self, request):
        cache_key = 'kaktus_yesterday_news'
        cached_data = cache.get(cache_key)

        if cached_data:
            return JsonResponse(cached_data)

        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        url = f'https://kaktus.media/?lable=8&date={yesterday}&order=time'

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        html = await response.text()
                        articles = await self._parse_articles(html)

                        # Получаем дату
                        date = await self._get_date(html)

                        result = {
                            'date': date,
                            'articles': articles,
                            'source': 'kaktus.media',
                            'last_updated': datetime.now().isoformat()
                        }

                        # Кэшируем на 24 часа (вчерашние новости не меняются)
                        cache.set(cache_key, result, timeout=86400)
                        return JsonResponse(result)
                    else:
                        return JsonResponse(
                            {'error': 'Failed to fetch news', 'status': response.status},
                            status=500
                        )
        except Exception as e:
            return JsonResponse(
                {'error': str(e), 'type': 'connection_error'},
                status=500
            )

    async def _get_date(self, html):
        soup = BeautifulSoup(html, 'lxml')
        date_element = soup.find('span', class_='PaginatorDate--today-text')
        return date_element.text.replace('  ', '') if date_element else (datetime.now() - timedelta(days=1)).strftime(
            "%d.%m.%Y")


class LatestNewsView(View, KaktusNewsMixin):
    """Последние новости с пагинацией"""

    async def get(self, request):
        page = int(request.GET.get('page', 1))
        per_page = int(request.GET.get('per_page', 10))
        cache_key = f'kaktus_latest_{page}_{per_page}'

        cached_data = cache.get(cache_key)
        if cached_data:
            return JsonResponse(cached_data)

        # Получаем как сегодняшние, так и вчерашние новости
        today_news = await self._fetch_news_for_date(datetime.now().strftime("%Y-%m-%d"))
        yesterday_news = await self._fetch_news_for_date((datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"))

        all_articles = today_news + yesterday_news

        # Применяем пагинацию
        start = (page - 1) * per_page
        end = start + per_page
        paginated_articles = all_articles[start:end]

        result = {
            'page': page,
            'per_page': per_page,
            'total_articles': len(all_articles),
            'articles': paginated_articles,
            'last_updated': datetime.now().isoformat()
        }

        # Кэшируем на 5 минут
        cache.set(cache_key, result, timeout=300)
        return JsonResponse(result)

    async def _fetch_news_for_date(self, date):
        url = f'https://kaktus.media/?lable=8&date={date}&order=time'
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        html = await response.text()
                        return await self._parse_articles(html)
        except Exception as e:
            print(f"Error fetching news for date {date}: {e}")
            return []