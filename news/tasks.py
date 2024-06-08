from datetime import datetime, timedelta

from celery import shared_task

from news.models import NewsArticle, Trend
from news.sentiment_analysis import get_sentiment_score
from news.trends import get_google_trends
from news.tsn_news import fetch_news
from settings.logger import AppLogger


@shared_task
def refresh_news():
    """Celery task to refresh trending news articles."""
    logger = AppLogger("refresh_news")
    try:
        # Fetch Google Trends
        get_google_trends()
        logger.write_info("Google Trends successfully updated.")

        # Fetch News from TSN
        fetch_news()
        logger.write_info("TSN news successfully updated.")

        # Analyze Sentiment Scores
        get_sentiment_score()
        logger.write_info("Sentiment scores successfully updated.")
    except Exception as error:
        logger.write_error(f"Error occurred during refresh_news task: {error}")
        raise


@shared_task
def delete_old_news_articles():
    """Celery task to delete news articles older than 7 days."""
    logger = AppLogger("delete_old_news_articles")
    try:
        seven_days_ago = datetime.now() - timedelta(days=7)
        old_articles = NewsArticle.objects.filter(publication_date__lt=seven_days_ago)
        old_articles.delete()
        logger.write_info("Old news articles successfully deleted.")
    except Exception as error:
        logger.write_error(
            f"Error occurred during delete_old_news_articles task: {error}"
        )
        raise


@shared_task
def delete_old_trends():
    """Celery task to delete trends older than 7 days."""
    logger = AppLogger("delete_old_trends")
    try:
        seven_days_ago = datetime.now() - timedelta(days=7)
        old_trends = Trend.objects.filter(date__lt=seven_days_ago)
        old_trends.delete()
        logger.write_info("Old trends successfully deleted.")
    except Exception as error:
        logger.write_error(f"Error occurred during delete_old_trends task: {error}")
        raise
