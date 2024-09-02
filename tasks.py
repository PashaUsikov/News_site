from celery import Celery
from celery.schedules import crontab

from webapp import create_app
from webapp.news.parsers import news_mail

flask_app = create_app()
celery_app = Celery('tasks', broker='redis://localhost:6379/0')


@celery_app.task
def news_mail_snippets():
    with flask_app.app_context():
        news_mail.get_news_snippets()


@celery_app.task
def news_mail_article():
    with flask_app.app_context():
        news_mail.save_news_article()


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(minute='*/5'), news_mail_snippets.s())
    sender.add_periodic_task(crontab(minute='*/5'), news_mail_article.s())

