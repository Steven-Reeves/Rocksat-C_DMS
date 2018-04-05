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
                
def alarm(run, count):
    print("Process timed out at count %i!") % count
                
def timer_test():
    count = 0
    run = True
    while run and count < 5:
        print("Count: %i") % count
        timer = Timer(3, alarm, (run, count))
        timer.start()
        time.sleep(count)
        timer.cancel()
        print("Count: %i completed.") % count
        count += 1
    if not run:
        print("Process ended at count " + str(count))
