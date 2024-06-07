from django.db import models


class Trend(models.Model):
    """Model for a news trend."""

    keyword = models.CharField("Keyword", max_length=255)
    date = models.DateField("Date")

    class Meta:
        unique_together = ("keyword", "date")

    def __str__(self):
        return self.keyword


class NewsArticle(models.Model):
    """Model for an individual news article."""

    title = models.CharField("Title", max_length=1000)
    link = models.URLField("Article URL", max_length=200, unique=True)
    publication_date = models.DateTimeField("Publication Date", null=True, blank=True)
    sentiment_score = models.FloatField("Sentiment Score", null=True, blank=True)
    trends = models.ManyToManyField(Trend, related_name="news_articles")

    def __str__(self):
        return f"{self.title} / {self.publication_date:%Y-%m-%d}"

    class Meta:
        verbose_name = "News article"
        verbose_name_plural = "News articles"
