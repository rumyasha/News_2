import django_filters
from datetime import datetime
from django.core.cache import cache


class NewsFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(
        method='filter_by_title',
        label='Поиск по названию (регистронезависимый)'
    )

    source = django_filters.CharFilter(
        field_name='source',
        lookup_expr='icontains',
        label='Фильтр по источнику'
    )

    # Фильтры по дате
    date = django_filters.DateFilter(
        method='filter_by_date',
        label='Фильтр по точной дате (YYYY-MM-DD)'
    )

    date_after = django_filters.DateFilter(
        method='filter_by_date_after',
        label='Новости после указанной даты'
    )

    date_before = django_filters.DateFilter(
        method='filter_by_date_before',
        label='Новости до указанной даты'
    )

    # Кастомные методы фильтрации
    def filter_by_title(self, queryset, name, value):
        return [article for article in queryset if value.lower() in article.get('title', '').lower()]

    def filter_by_date(self, queryset, name, value):
        return [article for article in queryset
                if article.get('date') and datetime.strptime(article['date'], '%Y-%m-%d').date() == value]

    def filter_by_date_after(self, queryset, name, value):
        return [article for article in queryset
                if article.get('date') and datetime.strptime(article['date'], '%Y-%m-%d').date() >= value]

    def filter_by_date_before(self, queryset, name, value):
        return [article for article in queryset
                if article.get('date') and datetime.strptime(article['date'], '%Y-%m-%d').date() <= value]

    # Метод для получения данных из кеша
    @property
    def qs(self):
        if not hasattr(self, '_queryset'):
            last_results = cache.get('last_news_results', {})
            all_articles = []

            for day in ['today', 'yesterday']:
                day_data = last_results.get(day, {})
                for article in day_data.get('articles', []):
                    article_with_date = article.copy()
                    article_with_date['date'] = day_data.get('date')
                    all_articles.append(article_with_date)

            self._queryset = all_articles

        return super().filter_queryset(self._queryset)

    class Meta:
        model = None  # Явно указываем, что модель не используется
        fields = ['title', 'date', 'date_after', 'date_before', 'source']