from datetime import datetime

import feedparser
import pytz
from django.utils import timezone

from news.models import Trend, NewsArticle
from news.utils import clean_text
from settings.logger import AppLogger


def fetch_news():
    """Get new posts from the tsn feed within the last 7 days and save trending news."""
    logger = AppLogger("tsn_feed")
    feed_url = "https://tsn.ua/rss/full.rss"
    seven_days_ago = timezone.now() - timezone.timedelta(days=7)

    try:
        news_feed = feedparser.parse(feed_url)
        current_trends = set(
            Trend.objects.filter(date__gte=seven_days_ago).values_list("id", "keyword")
        )
        trends_map = {
            trend[1]: trend[0] for trend in current_trends
        }  # keyword to id map
        trending_news = []

        for entry in news_feed.entries:
            if not hasattr(entry, "link"):
                continue

            published_date = datetime(*entry.published_parsed[:6])
            published_date = pytz.utc.localize(published_date)
            if published_date < seven_days_ago:
                continue

            cleaned_title = clean_text(entry.title)
            cleaned_full_text = clean_text(getattr(entry, "fulltext", ""))

            # Check if the article title or full text contains any of the current trend keywords
            matched_trends = [
                trends_map[trend]
                for trend in trends_map
                if trend in cleaned_title or trend in cleaned_full_text
            ]

            if matched_trends:
                trending_news.append(
                    (
                        NewsArticle(
                            title=entry.title,
                            link=entry.link,
                            publication_date=published_date,
                        ),
                        matched_trends,
                    )
                )

        news_to_create = [article for article, _ in trending_news]
        NewsArticle.objects.bulk_create(news_to_create, ignore_conflicts=True)

        # Add trends to articles
        for article, matched_trends in trending_news:
            existing_article = NewsArticle.objects.get(link=article.link)
            existing_article.trends.add(*matched_trends)
        logger.write_info(
            f"Successfully processed {len(trending_news)} news articles from TSN."
        )
    except Exception as error:
        error_message = f"Error occurred while fetching news from TSN: {error}"
        logger.write_error(error_message)
        raise Exception(error_message)
