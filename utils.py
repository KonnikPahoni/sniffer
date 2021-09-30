import datetime
import json
import logging
import threading
from django.core import serializers
import boto3
import pytz
import inspect
import data_getter
from data_getter.schemas.bfx import BFXTickerTradingModel
from settings import CONFIGURED_THREADS, REGION_NAME, SPACES_ENDPOINT_URL, BUCKET_NAME, UPLOAD_FOLDER_NAME
import os
import datetime as dt


def format_output(obj, as_string=False):
    if not as_string:
        return obj
    return json.dumps(obj)


def check_health(as_string=False):
    errors = []
    thread_names = list(map(lambda thread: thread.name, threading.enumerate()))

    for thread_name in CONFIGURED_THREADS:
        if thread_name not in thread_names:
            error_text = "Thread {0} is missing".format(thread_name)
            errors.append(error_text)

    if len(errors) == 0:
        logging.info('Health: OK')
        return format_output({"status": "OK"}, as_string)
    else:
        logging.warning('Health: errors' + str(errors))
        return format_output({"status": "error", "errors": errors}, as_string)


class TelegramHandler(logging.StreamHandler):

    def __init__(self, telegram_bot):
        super().__init__()
        self.telegram_bot = telegram_bot

    def emit(self, record):
        for setting in self.telegram_bot.admin_settings.filter(logging_level__lte=record.levelno):
            self.telegram_bot.send(setting.user.telegram_id, self.format(record))


def get_models():
    members = inspect.getmembers(data_getter.schemas, inspect.ismodule)
    models = []

    for member in members:
        schema_name = member[1].__name__.split('.')
        if len(schema_name) >= 3 and schema_name[0] == 'data_getter' and schema_name[1] == 'schemas':
            classes = inspect.getmembers(member[1], inspect.isclass)
            for cls in classes:
                models.append(cls[1])

    return models


def dump(date, remove=False):
    models = get_models()
    for model in models:
        filename = "var/celery/" + model.__name__ + "/" + date + ".json"

        start = datetime.datetime.strptime(date, '%Y-%m-%d').replace(tzinfo=pytz.UTC)

        end = start + dt.timedelta(days=1)

        objects = model.objects.filter(datetime__gte=start, datetime__lte=end)

        if len(objects) == 0:
            print('No ' + model.__name__ + ' data for ' + date)
            continue

        data = serializers.serialize("json", objects)

        if not os.path.exists("var/celery/" + model.__name__):
            os.mkdir("var/celery/" + model.__name__)

        f = open(filename, "w")
        f.write(data)
        f.close()

        session = boto3.session.Session()
        client = session.client('s3',
                                region_name=REGION_NAME,
                                endpoint_url=SPACES_ENDPOINT_URL,
                                aws_access_key_id=os.getenv('SPACES_KEY'),
                                aws_secret_access_key=os.getenv('SPACES_SECRET'))

        filesize = os.path.getsize(filename)
        s3_filename = UPLOAD_FOLDER_NAME + '/' + model.__name__ + '/' + date + ".json"
        print('Uploading file ' + filename + ' (' + '{:.3f}'.format(filesize / 1000 / 1000) + ' MB)')
        client.upload_file(filename, BUCKET_NAME, s3_filename)

        print('Verifying upload')
        resource = boto3.resource('s3',
                                  region_name=REGION_NAME,
                                  endpoint_url=SPACES_ENDPOINT_URL,
                                  aws_access_key_id=os.getenv('SPACES_KEY'),
                                  aws_secret_access_key=os.getenv('SPACES_SECRET')
                                  )
        object_summary = resource.ObjectSummary(BUCKET_NAME, s3_filename)
        if object_summary.size != filesize:
            logging.error('File size on server does not match original file size: ' + s3_filename)
        else:
            print('Object size verified. ' + model.__name__ + ' upload finished.')
            logging.info(model.__name__ + ' dump for ' + date + ' uploaded. Size: ' + str(
                filesize / 1000 / 1000) + ' MB')

            # Removing objects from Django (!)
            if remove:
                objects.delete()
