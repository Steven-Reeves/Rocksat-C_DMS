# Author:       Andy Horn
# Date:         4/4/2018
# Modified:     4/18/2018
# Filename:     DataThread.py
# Overview:     DataThread class that manages simultaneous threads

from threading import Thread, Timer
import time
import serial


class DataThread:

    def __init__(self):
        self.__threads = []
        self.run_list = []
        self.num_threads = 0
        self.started = False

    def main_timer_complete(self, thread_id):
        self.run_list[thread_id] = False
        print("[Thread {} timer] Countdown complete".format(thread_id))

    def reconnect(self, port, port_name, thread_id):
        print("[reconnect] Reconnecting to device {}".format(port_name))
        port.close()
        while not port.is_open and self.run_list[thread_id]:
            try:
                port.open()
                print("[reconnect] Connected!")
            except:
                time.sleep(.25)

    def __watch_threads(self):
        print("[Watcher] Activated")
        start_time = time.time()
        while self.__threads:
            for t in self.__threads:
                if not t.isAlive():
                    self.__threads.remove(t)
                    self.num_threads -= 1
            time.sleep(2)
        if not self.__threads:
            print("[Watcher] All threads complete.")
            print("[Watcher] Time to complete: " + str("%.2f" % (time.time() - start_time)))
            self.num_threads = 0
            self.started = False

    def read_serial(self, thread_id, port, baudrate=9600, filename='none', file_type='.txt'):
        exit_code = 0
        countdown = Timer(60, self.main_timer_complete, (thread_id,))
        countdown.start()
        start_time = time.time()
        if filename == 'none':
            filename = port
        try:
            with serial.Serial(port, baudrate, timeout=3, dsrdtr=True) as s:
                s.flush()
                with open(filename + file_type, 'ab') as file:
                    while self.run_list[thread_id]:
                        try:
                            if s.is_open:
                                buffer = s.readline()
                                if buffer.split():
                                    time_lapsed = time.time() - start_time
                                    file.write(buffer)
                                    print("[{}] {} {}".format(filename, str("%2f" % time_lapsed), str(buffer)))
                                else:
                                    print("[{}] 3 seconds no input".format(filename))
                        except serial.SerialException:
                            self.reconnect(s, port, thread_id)
        except KeyboardInterrupt:
            print("[{}] KeyboardInterrupt".format(port))
            exit_code = 1
        except serial.SerialException:
            print("[{}] Unable to connect".format(port))
            exit_code = 2
        finally:
            print("[{}] Exit Code {}".format(port, exit_code))
            self.run_list[thread_id] = False
            countdown.cancel()

    # *values will take any remaining values as a tuple
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
            try:
                for t in self.__threads:
                    self.run_list[index] = True
                    t.start()
                    index += 1
                self.started = True
                # Create independent thread to monitor other threads
                watch = Thread(target=self.__watch_threads)
                watch.start()
                watch.join() # Keep main process alive as long as child threads are active
            except KeyboardInterrupt:
                print("[DataThread] KeyboardInterrupt")
                self.stop()
                print("[DataThread] Stop() called")
            finally:
                print("[DataThread] All threads complete.")

    def stop(self):
        print("[Stop] Call received.")
        # self.run = False
        for n in range(len(self.run_list)):
            self.run_list[n] = False
            print("[DataThread] Flag set to false.")
