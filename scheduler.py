import time
import schedule
import threading
from settings import SCHEDULER_NAME


# This is a helper class to manage scheduled operations in a separate thread
class Scheduler:

    def __init__(self):
        self._stop_event = threading.Event()
        self._thread = threading.Thread(target=self.run_pending, name=SCHEDULER_NAME)

    def run_pending(self):
        while not self._stop_event.isSet():
            schedule.run_pending()
            time.sleep(0.1)

    def start(self):
        self._thread.start()

    def stop(self):
        self._stop_event.set()
