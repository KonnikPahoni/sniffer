import django
from celery import shared_task
from celery.schedules import crontab
from settings import BACKUP_DISTANCE
from utils import dump
from .celery import celery as celery_app
from .mappers.bfxticker import BFXTickerGetter
import datetime as dt


@celery_app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(30,
                             bfx_ticker.s(),
                             name='Bitfinex ticker')

    date_ = (dt.datetime.today() - dt.timedelta(days=BACKUP_DISTANCE)).strftime('%Y-%m-%d')

    sender.add_periodic_task(
        crontab(hour=7, minute=30),
        dump_database.s(date_),
        name='Dumping database'
    )


@celery_app.task()
def dump_database(date):
    dump(date)
    logging


@celery_app.task()
def bfx_ticker():
    return str(len(BFXTickerGetter().invoke())) + ' objects created'
