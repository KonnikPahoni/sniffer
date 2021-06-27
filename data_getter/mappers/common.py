import logging
import requests
from exceptions import GetRequestException, ObjectCreationException
import abc


class Getter(abc.ABC):
    # Url to retrieve objects from
    url = None

    response = None
    objects = []

    TIMEOUT_DEFAULT = 10

    def __init__(self, timeout=TIMEOUT_DEFAULT):
        self.timeout = timeout

    # Get raw data
    def get(self):
        try:
            request = requests.get(url=self.url, timeout=self.timeout)
            return request.json()
        except requests.exceptions.Timeout:
            logging.warning("Connection timeout")
        except requests.exceptions.ConnectionError:
            logging.warning("No connection")
        except Exception:
            raise GetRequestException
        return None

    # Every data getter should implement create_objects()
    @staticmethod
    @abc.abstractmethod
    def create_objects():
        pass

    def invoke(self):

        # Getting raw data
        self.response = self.get()

        if self.response:
            try:

                # Populating objects
                self.objects = self.create_objects()

                for object_ in self.objects:
                    object_.save()

            except Exception:
                raise ObjectCreationException

        return self.objects
