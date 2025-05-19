from celery import shared_task
from .parsers import KaktusMediaParser
import asyncio


@shared_task
def parse_kaktus_news_task():
    """Celery-задача для парсинга новостей"""

    async def async_parse():
        async with KaktusMediaParser() as parser:
            return await parser.fetch_news(days=2)

    loop = asyncio.new_event_loop()
    result = loop.run_until_complete(async_parse())
    loop.close()
    return result