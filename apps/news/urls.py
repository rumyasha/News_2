from django.urls import path
from .views import TodayNewsView, YesterdayNewsView, LatestNewsView

urlpatterns = [
    path('today/', TodayNewsView.as_view(), name='today-news'),
    path('yesterday/', YesterdayNewsView.as_view(), name='yesterday-news'),
    path('latest/', LatestNewsView.as_view(), name='latest-news'),
]