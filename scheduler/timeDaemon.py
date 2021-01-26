import datetime
import threading
import time


class TimeDaemon:
    def __init__(self, min_every_sec, update_time_signal):
        self._current_time = datetime.datetime.now()
        self._running = True
        self._min_every_sec = min_every_sec
        self._update_time_signal = update_time_signal

    def run(self):
        while self._running:
            self._current_time = self._current_time + datetime.timedelta(
                minutes=self._min_every_sec)
            self._update_time_signal.emit(self._current_time.strftime("%H:%M:%S %d/%m/%Y"))
            time.sleep(1)

    def get_current_time(self):
        return self._current_time

    def display_current_time(self):
        print(str(self._current_time))

    def stop_time_daemon(self):
        self._running = False
