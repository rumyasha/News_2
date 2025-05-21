# news/api/views.py
from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend
from .filters import NewsFilter
from rest_framework.permissions import IsAuthenticated


class NewsFilterAPIView(ListAPIView):
    """
    Unified API endpoint for news with filtering capabilities
    Supports:
    - /api/news/
    - /api/filter/
    - /api/status/
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = NewsFilter

    def get_queryset(self):
        # Queryset is handled in filters.py
        return []