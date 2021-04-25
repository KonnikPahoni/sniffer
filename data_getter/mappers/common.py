import logging
import requests
from exceptions import GetRequestException, ObjectCreationException


class Getter:
    url = None
    response = None
    objects = []

    TIMEOUT_DEFAULT = 10

    def __init__(self, timeout=TIMEOUT_DEFAULT):
        self.timeout = timeout

    def get(self):
        try:
            request = requests.get(url=self.url, timeout=self.timeout)
            return request.json()
        except requests.exceptions.Timeout:
            logging.warning("Connection timeout")
        except Exception:
            raise GetRequestException
        return None

    def save_to_cache(self):
        pass

    def add_to_queue(self):
        pass

    @staticmethod
    def map():
        return None

    def invoke(self):
        logging.info("invoke")
        self.response = self.get()
        if self.response:
            print("response received")
            try:
                self.objects = self.map()
            except Exception:
                raise ObjectCreationException

            self.add_to_queue()
