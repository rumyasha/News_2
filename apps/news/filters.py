from rest_framework.filters import BaseFilterBackend


class NewsFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        # Фильтр по заголовку
        if title := request.query_params.get('title'):
            queryset = [n for n in queryset if title.lower() in n['title'].lower()]

        # Фильтр по дате (формат YYYY-MM-DD)
        if date := request.query_params.get('date'):
            queryset = [n for n in queryset if n.get('date') == date]

        # Фильтр по источнику
        if source := request.query_params.get('source'):
            queryset = [n for n in queryset if n.get('source') == source]

        return queryset