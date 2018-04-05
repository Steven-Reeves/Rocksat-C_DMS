# Author:	Andy Horn
# Date:		4/4/2018
# Modified:	4/4/2018

# Purpose:	Create functions to test threading.

import time
from threading import Timer

def print_time(title='default', cycles=3, delay=1):
	for i in range(cycles):
		print(title + ": " + time.ctime(time.time()))
		time.sleep(delay)
                
def alarm(count, run):
    print("Process timed out at count %i!") % count
    del run[0] # acts like pass-by-reference, removes only value in list
    # essentially turning run into a False boolean
                
def timer_test():
    count = 0
    run = [1] # allows 'alarm' method to impact this method
    # Python normally uses pass-by-value, passing a list will
    # simulate passing by reference.
    while run and count < 5:
        print("Count: %i") % count
        timer = Timer(3, alarm, (count, run))
        timer.start()
        time.sleep(count)
        timer.cancel()
        print("Count: %i completed.") % count
        if run:
            count += 1
    if not run:
        print("Process ended at count " + str(count))
    if count == 5:
        print("Count reached 5")
