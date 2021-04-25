import json
import logging
import threading
from settings import CONFIGURED_THREADS


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
