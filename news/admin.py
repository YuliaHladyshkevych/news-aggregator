from django.contrib import admin

from news.models import NewsArticle, Trend


@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    ordering = ["-publication_date"]


@admin.register(Trend)
class TrendAdmin(admin.ModelAdmin):
    ordering = ["-date"]
