# Author:       Andy Horn
# Date:         4/4/2018
# Modified:     4/8/2018
# Filename:     DataThread.py
# Overview:     DataThread class that manages simultaneous threads

from threading import Thread
import time

class DataThread:

    def __init__(self):
        self.__threads = []
        self.num_threads = 0
        self.started = False

    @staticmethod
    def __watch_threads(self):
        start_time = time.time()
        while self.__threads:
            for t in self.__threads:
                if not t.isAlive():
                    self.__threads.remove(t)
                    self.num_threads -= 1
        if not self.__threads:
            print("[Watcher] All threads complete.")
            print("[Watcher] Time to complete: " + str("%.2f" % (time.time() - start_time)))
            self.num_threads = 0
            self.started = False


    # *vals will take any remaining values as a tuple
    def add_thread(self, func, *vals):
        if not self.started:
            t = Thread(target=func, args=vals)
            self.__threads.append(t)
            self.num_threads += 1
        else:
            print("[add_thread] Cannot add threads while running.")

    def start(self):
        try:
            for t in self.__threads:
                #t.daemon = True
                t.start()
            self.started = True
                # Create independent thread to monitor other threads
            watch =  Thread(target=self.__watch_threads, args=(self,))
            watch.start()
            watch.join()
        except KeyboardInterrupt:
            print("[DataThread] KeyboardInterrupt")
            raise KeyboardInterrupt
        finally:
            print("[DataThread] All threads complete.")
