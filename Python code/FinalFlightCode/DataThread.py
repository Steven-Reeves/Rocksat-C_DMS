# Author:       Andy Horn
# Date:         4/4/2018
# Modified:     6/2/2018
# Filename:     DataThread.py
# Overview:     DataThread class that manages simultaneous threads

from threading import Thread, Timer
import time
import serial


class DataThread:

    def __init__(self):
        self.__threads = [] # container for all the independent threads
        self.run_list = [] # container for flags used by each thread
        self.num_threads = 0 # total number of threads
        self.started = False # 'killswitch' for all threads

    # called when thread's master timer runs out, kills the thread
    def main_timer_complete(self, thread_id):
        self.run_list[thread_id] = False
        print("[Thread {} timer] Countdown complete".format(thread_id))

    # called when the serial read times out
    def reconnect(self, port, port_name, thread_id):
        print("[reconnect] Reconnecting to device {}".format(port_name))
        port.close() # force the port to close
        while not port.is_open and self.run_list[thread_id]:
            try:
                port.open() # reopen the port, if unsuccessful will loop through and try again
                print("[reconnect] " + port_name + ": Connected!")
            except:
                time.sleep(.25)

    # creates a thread to 'watch' all other threads, keeps DataThread class alive
    def __watch_threads(self):
        print("[Watcher] Activated")
        start_time = time.time()
        while self.__threads: # while threads exist:
            for t in self.__threads:
                if not t.isAlive():
                    self.__threads.remove(t) # remove 'dead' threads from container
                    self.num_threads -= 1 # decrement number of threads (may not be needed)
            time.sleep(2) # rest for 2 seconds, otherwise will use up CPU power
        if not self.__threads: # when all threads are removed, kill DataThread:
            print("[Watcher] All threads complete.")
            print("[Watcher] Time to complete: " + str("%.2f" % (time.time() - start_time)))
            self.num_threads = 0
            self.started = False

    # PRIMARY THREAD FUNCTION #
    def read_serial(self, thread_id, port, baudrate=9600, filename='none', file_type='.txt'):
        exit_code = 0 # exit code variable; 0 = success, 1 = keyboard interrupt, 2 = serial disconnect
        countdown = Timer(1500, self.main_timer_complete, (thread_id,)) # master timer for thread (in seconds)
        countdown.start()
        start_time = time.time()
        if filename == 'none':
            filename = port
        try:
            # open serial port with 3 second timeout, dsrdtr=True will prevent restarting the Arduino
            serial_success = False
            while serial_success is not True and self.run_list[thread_id]:
                try:
                    s = serial.Serial(port, baudrate, timeout=3, dsrdtr=True)
                    s.close()
                    serial_success = True
                except serial.SerialException:
                    print(str("%2f" % (time.time() - start_time)) + " Port: " + port + " unable to connect!")
                    time.sleep(1)
            with serial.Serial(port, baudrate, timeout=3, dsrdtr=True) as s:
                s.flush() # flush before attempting first read
                with open(filename + file_type, 'ab') as file: # open binary file, append new data
                    while self.run_list[thread_id]: # check flag at correct index
                        try:
                            if s.is_open: # if serial port open:
                                buffer = s.readline() # read serial data
                                if buffer.split(): # if buffer contains data:
                                    time_lapsed = time.time() - start_time # get timestamp
                                    file.write(buffer) # write the serial buffer to the binary file
                                    #print("[{}] {} {}".format(filename, str("%2f" % time_lapsed), str(buffer)))
                                else: # if no data present, print error message
                                    print("[{}] 3 seconds no input".format(filename))
                        except serial.SerialException:
                            # if the serial port is not connected, run connection method
                            self.reconnect(s, port, thread_id)
        except KeyboardInterrupt:
            # on keyboard interrupt, print error message
            print("[{}] KeyboardInterrupt".format(port))
            exit_code = 1
        except serial.SerialException:
            # if serial connection fails at very beginning, print error message
            print("[{}] Unable to connect".format(port))
            exit_code = 2
        finally:
            # at very end, print status message, disable flag, cancel timer
            print("[{}] Exit Code {}".format(port, exit_code))
            self.run_list[thread_id] = False
            countdown.cancel()

    # *values will take any remaining values as a tuple
    def add_thread(self, *values):
        arg_list = list(values) # convert tuple to list
        insert = [self.num_threads] # get new thread's ID
        arg_list[:0] = insert # insert new thread's ID at beginning of list
        new_values = tuple(arg_list) # convert list back to tuple
        if not self.started: # only add threads while none are running
            t = Thread(target=self.read_serial, args=new_values) # create new thread
            self.__threads.append(t) # add new thread to container
            self.run_list.append(False) # add and set new thread's flag
            self.num_threads += 1 # increment counter
        else:
            print("[add_thread] Cannot add threads while running.")

    # start all prepared threads
    def start(self):
        if self.__threads: # if threads exist in container
            index = 0
            try:
                for t in self.__threads:
                    self.run_list[index] = True # set each thread's flag
                    t.start() # start each thread
                    index += 1 # set index for next thread's flag
                self.started = True # once all threads are started, set master flag
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

    # stop all threads
    def stop(self):
        print("[Stop] Call received.")
        for n in range(len(self.run_list)):
            self.run_list[n] = False # set each thread's flag to False
            print("[DataThread] Flag set to false.")
