from threading import Thread
import time

class DataThread:

    def __init__(self):
        self.threads = []
        self.watch = []
        self.num_threads = 0
        self.started = False

    @staticmethod
    def watch_threads(self):
        start_time = time.time()
        while self.threads:
            # print("THREADS REMAINING: " + str(len(threads)))
            for t in self.threads:
                if not t.isAlive():
                    self.threads.remove(t)
        if not self.threads:
            print("All threads complete.")
            self.num_threads = 0
            print("Time to complete: " + str("%.2f" % (time.time() - start_time)))


    # *vals will take any remaining values as a tuple
    def add_thread(self, func, *vals):
        if not self.started:
            t = Thread(target=func, args=vals)
            self.threads.append(t)
            self.num_threads += 1
        else:
            print("Cannot add new thread after starting")

    def start(self, empty=False):
        for t in self.threads:
            t.start()
        self.started = True
        if empty:
            Thread(target=self.watch_threads, args=(self,)).start()

    def purge(self):
        self.threads.clear()
        self.started = False