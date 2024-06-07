from rest_framework import serializers

from news.models import NewsArticle, Trend


class TrendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trend
        fields = ["keyword", "date"]


class NewsArticleSerializer(serializers.ModelSerializer):
    trends = TrendSerializer(many=True, read_only=True)

    class Meta:
        model = NewsArticle
        fields = ["title", "link", "publication_date", "sentiment_score", "trends"]
