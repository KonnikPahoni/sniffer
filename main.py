from settings import *
import logging
import schedule
from telegram_bot import TelegramBot
from utils import TelegramHandler, check_health
import threading


class Sniffer:

    def __init__(self):
        self.telegram_bot = TelegramBot()

        log_formatter = logging.Formatter("%(asctime)s [%(threadName)s] [%(levelname)s]  %(message)s")
        logger = logging.getLogger()

        telegram_handler = TelegramHandler(self.telegram_bot)
        telegram_handler.setFormatter(log_formatter)
        telegram_handler.setLevel(LOGGING_LEVEL_TELEGRAM)
        logger.addHandler(telegram_handler)

        file_handler = logging.FileHandler(PATH_TO_LOGS)
        file_handler.setFormatter(log_formatter)
        file_handler.setLevel(LOGGING_LEVEL_FILE)
        logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(log_formatter)
        console_handler.setLevel(LOGGING_LEVEL_CONSOLE)
        logger.addHandler(console_handler)

        # Set global logging level, can be equal to 0
        logger.setLevel(logging.DEBUG)

        schedule.every(HEALTH_CHECK_INTERVAL).seconds.do(check_health)

    def start(self):
        self.telegram_bot.start()
        self.telegram_bot.send_all_admins('App launched. Status: ' + check_health()['status'])

    def stop(self):
        self.telegram_bot.stop()


if __name__ == "__main__":
    sniffer = Sniffer()
    sniffer.start()
