from datetime import datetime

from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from .parsers import KaktusMediaParser
import asyncio


class NewsAdminSite(admin.AdminSite):
    site_header = "Администрирование новостного агрегатора"
    site_title = "Новостной агрегатор"
    index_title = "Управление новостями"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('parse-news/', self.admin_view(self.parse_news_view),
                 path('news-status/', self.admin_view(self.news_status_view))),
        ]
        return custom_urls + urls

    async def _parse_news(self, request):
        """Асинхронный парсинг новостей"""
        async with KaktusMediaParser() as parser:
            today_news = await parser.get_today_news()
            yesterday_news = await parser.get_yesterday_news()

            request.session['last_parsed_news'] = {
                'today': today_news,
                'yesterday': yesterday_news,
                'parsed_at': datetime.now().isoformat()
            }

            return len(today_news['articles']) + len(yesterday_news['articles'])

    def parse_news_view(self, request):
        """View для ручного парсинга новостей"""
        if request.method == 'POST':
            try:
                # Запускаем асинхронный парсинг
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                news_count = loop.run_until_complete(self._parse_news(request))
                loop.close()

                messages.success(
                    request,
                    f"Успешно спаршено {news_count} новостей (сегодня + вчера)"
                )
            except Exception as e:
                messages.error(request, f"Ошибка при парсинге: {str(e)}")

            return HttpResponseRedirect('../parse-news/')

        last_parsed = request.session.get('last_parsed_news', {})
        context = {
            **self.each_context(request),
            'last_parsed': last_parsed,
            'opts': {'app_label': 'news'},
        }
        return render(request, 'admin/news_parse.html', context)

    def news_status_view(self, request):
        """Статистика по новостям"""
        last_parsed = request.session.get('last_parsed_news', {})

        today_count = len(last_parsed.get('today', {}).get('articles', []))
        yesterday_count = len(last_parsed.get('yesterday', {}).get('articles', []))

        context = {
            **self.each_context(request),
            'today_count': today_count,
            'yesterday_count': yesterday_count,
            'last_parsed_at': last_parsed.get('parsed_at'),
            'opts': {'app_label': 'news'},
        }
        return render(request, 'admin/news_status.html', context)


# Создаем экземпляр кастомной админки
news_admin_site = NewsAdminSite(name='news_admin')