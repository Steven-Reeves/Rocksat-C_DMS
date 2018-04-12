# Author:       Andy Horn
# Date:         4/4/2018
# Modified:     4/8/2018
# Filename:     DataThread.py
# Overview:     DataThread class that manages simultaneous threads

from threading import Thread, Timer
import time, serial


class DataThread:

    def __init__(self):
        self.__threads = []
        self.run_list = []
        self.num_threads = 0
        self.started = False
        self.run = False

    def main_timer_complete(self, thread_id):
        self.run_list[thread_id] = False
        print("[Thread {} timer] Countdown complete.".format(thread_id))

    def serial_read_timeout(self, port, name):
        print("[Timeout] Device [{}] is unresponsive, flushing port.".format(name))
        port.flush()
        print("[Timeout] Port flushed")

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

    def read_serial(self, thread_id, port, baudrate=9600, filename='none', file_type='.txt', wait_time=2, retries=1):
        num_failures = 0
        countdown = Timer(60, self.main_timer_complete, (thread_id,))
        countdown.start()
        start_time = time.time()
        if filename == 'none':
            filename = port
        try:
            with serial.Serial(port, baudrate, timeout=wait_time * 2, dsrdtr=True) as s:
                with open(filename + file_type, 'a') as file:
                    while self.run_list[thread_id]:
                        if wait_time > 0:
                            timer = Timer(wait_time, self.serial_read_timeout, (s, port))
                            timer.start()
                        buffer = s.readline().decode('ascii')
                        # buffer = s.readline()
                        s.flush()
                        if wait_time > 0:
                            timer.cancel()
                        if buffer.split():
                            file.write(str(time.time() - start_time) + str(buffer))
                            print("[{}] {}".format(port, buffer))
                        else:
                            print("[{}] No input".format(port))
                            num_failures += 1
                            if num_failures > retries:
                                print("Device [{}] has failed, exiting thread.".format(port))
                                self.run_list[thread_id] = False
                                # break
        except KeyboardInterrupt:
            print("[read_serial] KeyboardInterrupt")
        # except:
        # print("[read_serial] Unhandled Exception")
        finally:
            print("[read_serial] Exit Code 0")

    # *vals will take any remaining values as a tuple
    def add_thread(self, *values):
        arg_list = list(values)
        insert = [self.num_threads]
        arg_list[:0] = insert
        new_values = tuple(arg_list)
        if not self.started:
            t = Thread(target=self.read_serial, args=new_values)
            self.__threads.append(t)
            self.run_list.append(False)
            self.num_threads += 1
        else:
            print("[add_thread] Cannot add threads while running.")

    def start(self):
        if self.__threads:
            index = 0
            self.run = True
            try:
                for t in self.__threads:
                    self.run_list[index] = True
                    t.start()
                    index += 1
                self.started = True
                # Create independent thread to monitor other threads
                watch = Thread(target=self.__watch_threads, args=(self,)).start()
                # watch.start()
                # watch.join()
            except KeyboardInterrupt:
                print("[DataThread] KeyboardInterrupt")
                raise KeyboardInterrupt
            finally:
                print("[DataThread] All threads complete.")

    def stop(self):
        self.run = False
        for flag in self.run_list:
            flag = False
