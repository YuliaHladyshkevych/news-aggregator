import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.settings")

app = Celery("news-aggregator")

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f"Request: {self.request!r}")


app.conf.beat_schedule = {
    "refresh_news": {
        "task": "news.tasks.refresh_news",
        "schedule": crontab(minute="*"),
    },
    "delete_old_news_articles": {
        "task": "news.tasks.delete_old_news_articles",
        "schedule": crontab(minute="0", hour="0"),
    },
    "delete_old_trends": {
        "task": "news.tasks.delete_old_trends",
        "schedule": crontab(minute="0", hour="0"),
    },
}
