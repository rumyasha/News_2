from django.urls import path
from .views import TodayNewsView, LatestNewsView

urlpatterns = [
    path('today/', TodayNewsView.as_view(), name='today-news'),
    path('latest/', LatestNewsView.as_view(), name='latest-news'),
]