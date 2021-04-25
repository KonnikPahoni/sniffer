from .celery import celery
from celery.schedules import crontab
import logging
from .mappers.bfxticker import BFXTickerGetter


@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(10.0, BFXTickerGetter(timeout=10).invoke(), name='BFX Ticker periodic task')
    logging.info("invoke")
    # Calls test('world') every 30 seconds
    # sender.add_periodic_task(30.0, test.s('world'), expires=10)

    # Executes every Monday morning at 7:30 a.m.
    # sender.add_periodic_task(
    #     crontab(hour=7, minute=30, day_of_week=1),
    #     test.s('Happy Mondays!'),
    # )


@celery.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
