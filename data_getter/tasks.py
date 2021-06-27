import logging
import pytz
from celery.schedules import crontab
import boto3
from settings import BACKUP_DISTANCE
from .celery import celery as celery_app
from django.core import serializers
from .mappers.bfxticker import BFXTickerGetter
from .schemas.bfx import BFXTickerTradingModel, BFXTickerFundingModel
import os
import datetime as dt


@celery_app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(10, bfx_ticker.s(), name='Bitfinex ticker')

    date_ = (dt.datetime.today() - dt.timedelta(days=BACKUP_DISTANCE)).strftime('%Y-%m-%d')

    sender.add_periodic_task(
        crontab(hour=7, minute=30),
        dump_database.s(date_),
        name='Dumping database'
    )

    sender.add_periodic_task(10, dump_database.s(date_), name='123r')


@celery_app.task()
def dump_database(date):
    models = [BFXTickerTradingModel, BFXTickerFundingModel]
    for model in models:
        filename = "var/celery/" + model.__name__ + date + ".json"

        timezone = pytz.timezone('UTC')
        today = dt.datetime.now(tz=timezone)
        start = today.replace(hour=0, minute=0, second=0, microsecond=0)
        end = start + dt.timedelta(days=0)

        data = serializers.serialize("json", model.objects.filter(datetime__gte=start, datetime__lte=end))
        f = open(filename, "w")
        f.write(data)
        f.close()

        session = boto3.session.Session()
        client = session.client('s3',
                                region_name='fra1',
                                endpoint_url='https://fra1.digitaloceanspaces.com',
                                aws_access_key_id=os.getenv('SPACES_KEY'),
                                aws_secret_access_key=os.getenv('SPACES_SECRET'))
        print('Uploading file ' + filename)
        client.upload_file(filename, 'sniffer', 'sniffer/' + model.__name__ + date + ".json")

        response = client.list_objects(Bucket='sniffer')
        for obj in response['Contents']:
            print(obj['Key'])

        logging.info(model.__name__ + ' dump for ' + date + ' uploaded. Size: ' + str(
            os.path.getsize(filename) / 1000000) + ' MB')


@celery_app.task()
def bfx_ticker():
    return str(len(BFXTickerGetter().invoke())) + ' objects created'
