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

    def __watch_threads(self):
        print("[Watcher] Activated")
        start_time = time.time()
        while self.__threads:
           # print("[Watcher] Watching")
            for t in self.__threads:
                if not t.isAlive():
                    self.__threads.remove(t)
                    self.num_threads -= 1
            time.sleep(1)
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
                s.flush()
                with open(filename + file_type, 'ab') as file:
                    while self.run_list[thread_id]:
                        if wait_time > 0:
                            timer = Timer(wait_time, self.serial_read_timeout, (s, port))
                            timer.start()
                        # buffer = s.readline().decode('ascii')
                        buffer = s.readline()
                        #s.flush()
                        if wait_time > 0:
                            timer.cancel()
                        if buffer.split():
                            time_lapsed = time.time() - start_time
                            #file.write(str(time_lapsed))
                            file.write(buffer)
                            print("[{}] {} {}".format(port, str(time_lapsed), str(buffer)))
                        else:
                            print("[{}] No input".format(port))
                            num_failures += 1
                            if num_failures > retries:
                                print("Device [{}] has failed, exiting thread.".format(port))
                                self.run_list[thread_id] = False
                                # break
        except KeyboardInterrupt:
            print("[read_serial] KeyboardInterrupt")
            self.run_list[thread_id] = False
            countdown.cancel()
        # except:
        # print("[read_serial] Unhandled Exception")
        finally:
            print("[read_serial] Exit Code 0")
            countdown.cancel()

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
                watch = Thread(target=self.__watch_threads)
                #watch.daemon = True
                watch.start()
                watch.join()
            except KeyboardInterrupt:
                print("[DataThread] KeyboardInterrupt")
                #raise KeyboardInterrupt
                self.stop()
                print("[DataThread] Stop() called")
            finally:
                print("[DataThread] All threads complete.")

    def stop(self):
        print("[Stop] Call received.")
        self.run = False
        for n in range(len(self.run_list)):
            self.run_list[n] = False
            print("[DataThread] Flag set to false.")
