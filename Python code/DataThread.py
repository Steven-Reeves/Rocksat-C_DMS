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
            for t in self.threads:
                if not t.isAlive():
                    self.__threads.remove(t)
                    self.num_threads -= 1
        if not self.__threads:
            print("All threads complete.")
            print("Time to complete: " + str("%.2f" % (time.time() - start_time)))
            self.num_threads = 0
            self.started = False


    # *vals will take any remaining values as a tuple
    def add_thread(self, func, *vals):
        if not self.started:
            t = Thread(target=func, args=vals)
            self.__threads.append(t)
            self.num_threads += 1
        else:
            print("Cannot add threads while running.")

    def start(self, empty=False):
        for t in self.__threads:
            t.start()
        self.started = True
        if empty:
            # Create independent thread to monitor other threads
            Thread(target=self.__watch_threads, args=(self,)).start() 

    def purge(self):
        self.__threads.clear()
        self.started = False