from django.urls import path
from .views import (
    NewsParseAPIView,
    TaskStatusAPIView,
    NewsFilterAPIView  # Используем единый View для фильтрации
)

urlpatterns = [
    # Эндпоинты управления парсингом
    path('parse/', NewsParseAPIView.as_view(), name='news-parse'),
    path('tasks/<str:task_id>/', TaskStatusAPIView.as_view(), name='task-status'),

    # Единый эндпоинт для работы с новостями (фильтрация/поиск)
    path('news/', NewsFilterAPIView.as_view(), name='news-filter'),

    # Альтернативные пути для обратной совместимости (можно удалить после обновления клиентов)
    path('filter/', NewsFilterAPIView.as_view(), name='news-filter-legacy'),
    path('status/', NewsFilterAPIView.as_view(), name='news-status-legacy'),
]