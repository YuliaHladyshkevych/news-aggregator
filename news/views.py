from rest_framework import generics
from rest_framework.pagination import PageNumberPagination

from news.models import NewsArticle
from news.serializers import NewsArticleSerializer


class TrendNewsPagination(PageNumberPagination):
    page_size = 20
    max_page_size = 100


class TrendNewsListView(generics.ListAPIView):
    """View to list trending news articles sorted by sentiment score."""

    serializer_class = NewsArticleSerializer
    pagination_class = TrendNewsPagination
    queryset = NewsArticle.objects.exclude(sentiment_score__isnull=True).order_by(
        "-sentiment_score"
    )
