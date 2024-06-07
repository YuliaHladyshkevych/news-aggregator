from datetime import datetime

import feedparser

from news.models import Trend
from news.utils import clean_text
from settings.logger import AppLogger


def get_google_trends():
    """Get Google trends in Ukraine and create Trend objects."""
    logger = AppLogger("google_trends")
    trends_url = "https://trends.google.com/trends/trendingsearches/daily/rss?geo=UA"

    try:
        trends = feedparser.parse(trends_url)
        trend_to_create = [
            Trend(
                keyword=clean_text(entry.title),
                date=datetime(*entry.published_parsed[:3]).date(),
            )
            for entry in trends.entries
        ]
        Trend.objects.bulk_create(trend_to_create, ignore_conflicts=True)
        logger.write_info("Google trends successfully retrieved and saved.")
    except Exception as error:
        error_message = f"Error occurred while searching for google trends: {error}"
        logger.write_error(error_message)
        raise Exception(error_message)
