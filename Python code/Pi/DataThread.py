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

    #staticmethod
    def read_serial(port, baudrate=9600, filename='none', file_type='.txt', wait_time=2, retries=1):
        num_failures = 0
        run = ['1']
        countdown = Timer(60, mainTimerComplete, (run,))
        countdown.start()
        start_time = time.time()
        if filename == 'none':
            filename = port
        try:
            with serial.Serial(port, baudrate, timeout=wait_time * 2, dsrdtr=True) as s:
                with open(filename + file_type, 'a') as file:
                    while run:
                        if wait_time > 0:
                            timer = Timer(wait_time, serialReadTimeout, (s, port))
                            timer.start()
                        # buffer = s.readline().decode('ascii')
                        buffer = s.readline()
                        s.flush()
                        if wait_time > 0:
                            timer.cancel()
                        if buffer.split():
                            file.write(str(time.time() - start_time) + str(buffer))
                            print("[{}] {}".format(port, str(buffer)))
                        else:
                            print("[{}] No input".format(port))
                            num_failures += 1
                            if num_failures > retries:
                                print("Device [{}] has failed, exiting thread.".format(port))
                                del run[0]
                                # break
        except KeyboardInterrupt:
            print("[read_serial] KeyboardInterrupt")
        # except:
        # print("[read_serial] Unhandled Exception")
        finally:
            print("[read_serial] Exit Code 0")

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
            watch =  Thread(target=self.__watch_threads, args=(self,)).start()
#            watch.start()
            watch.join()
        except KeyboardInterrupt:
            print("[DataThread] KeyboardInterrupt")
            raise KeyboardInterrupt
        finally:
            print("[DataThread] All threads complete.")
