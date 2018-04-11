# Thanks to Phillipe F. on StackOverflow:
# https://www.stackoverflow.com/questions/323972/is-there-any-way-to-kill-a-thread-in-python

import threading

class StopThread(threading.Thread):
    def __init__(self):
        super(StopThread, self).__init__(self)
        self.__stop_flag = threading.Event()

    def stop(self):
        self.__stop_flag.set()

    def is_stopped(self):
        return self.__stop_flag.is_set()
