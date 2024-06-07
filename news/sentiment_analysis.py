import re
from datetime import datetime, timedelta

import requests
from django.conf import settings

from news.models import NewsArticle
from settings.logger import AppLogger


def get_sentiment_score():
    """Get sentiment score for a given text using ChatGPT API."""
    logger = AppLogger("sentiment_score")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
    }
    articles = NewsArticle.objects.filter(
        publication_date__gte=datetime.now() - timedelta(days=7),
        sentiment_score__isnull=True,
    )

    for article in articles:
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful assistant analyzing sentiment. Score the sentiment from -1 (very negative) to 1 (very positive). Respond with only the sentiment score as a number.",
                },
                {
                    "role": "user",
                    "content": f"Analyze the sentiment of this news title: {article}",
                },
            ],
            "max_tokens": 250,
        }

        response = requests.post(settings.OPENAI_API_URL, headers=headers, json=data)
        if response.status_code == 200:
            response_json = response.json()
            message_content = response_json["choices"][0]["message"]["content"]

            # Extract sentiment score from response
            score_match = re.search(
                r"[-+]?(?:1(?:[.,]0+)?|0(?:[.,]\d+)?|[.,]\d+)", message_content
            )
            if score_match:
                sentiment = float(score_match.group().replace(",", "."))
            else:
                sentiment = 0.0
                logger.write_error(
                    f"No valid sentiment score found in response: {message_content}"
                )
            article.sentiment_score = sentiment
            article.save()
            logger.write_info(
                f"Successfully analyzed sentiment for article: {article.title}, Score: {sentiment}"
            )
        else:
            logger.write_error(
                f"Failed to get response from OpenAI API. Status code: {response.status_code}"
            )
