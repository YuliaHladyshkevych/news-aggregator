from django.urls import path

from news.views import TrendNewsListView

urlpatterns = [
    path("api/trending-news/", TrendNewsListView.as_view(), name="trending-news-list"),
]

app_name = "news"
