from .celery import celery as celery_app
from django_celery_beat.models import PeriodicTask, IntervalSchedule
import logging
from .mappers.bfxticker import BFXTickerGetter


@celery_app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(10, bfx_ticker.s(), name='Bitfinex ticker')


@celery_app.task()
def get_and_save_to_database(task):
    result = task.delay()
    bef_ticker_models = BFXTickerGetter().invoke()
    return bef_ticker_models


@celery_app.task(serializer='pickle')
def bfx_ticker():
    bef_ticker_models = BFXTickerGetter().invoke()
    return bef_ticker_models


@celery_app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
