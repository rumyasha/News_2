from .parsers import KaktusMediaParser
from django.core.cache import cache
import asyncio



def parse_kaktus_news_task():
    """Celery задача для парсинга новостей"""

    async def async_parse():
        async with KaktusMediaParser() as parser:
            return await parser.fetch_news(days=2)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(async_parse())
    loop.close()

    # Кешируем результаты
    cache.set('last_news_results', {
        'today': result.get('today', {}),
        'yesterday': result.get('yesterday', {}),
        'last_updated': result.get('last_updated')
    }, timeout=86400)  # Кеш на 24 часа

    return result
