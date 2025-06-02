<<<<<<< HEAD
from django.http import JsonResponse
from django.views import View
from django.core.cache import cache
=======
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .parsers import KaktusMediaParser
>>>>>>> b9fc818 (fafsa)
from datetime import datetime, timedelta
import asyncio


class NewsBaseView(APIView):
    permission_classes = [IsAuthenticated]
    parser_class = KaktusMediaParser

    async def get_news(self, date):
        async with self.parser_class() as parser:
            return await parser.fetch_news(date)


class TodayNewsView(NewsBaseView):
    """Новости за сегодня"""

    def get(self, request):
        try:
            loop = asyncio.new_event_loop()
            news_data = loop.run_until_complete(self.get_news(datetime.now()))
            loop.close()
            return Response(news_data)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class LatestNewsView(NewsBaseView):
    """Последние новости с пагинацией"""

    def get(self, request):
        try:
            page = int(request.query_params.get('page', 1))
            per_page = int(request.query_params.get('per_page', 10))

            loop = asyncio.new_event_loop()
            today = loop.run_until_complete(self.get_news(datetime.now()))
            yesterday = loop.run_until_complete(
                self.get_news(datetime.now() - timedelta(days=1))
            )
            loop.close()

            all_articles = today['articles'] + yesterday['articles']
            start = (page - 1) * per_page
            paginated = all_articles[start:start + per_page]

            return Response({
                'page': page,
                'per_page': per_page,
                'total': len(all_articles),
                'articles': paginated
            })
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )