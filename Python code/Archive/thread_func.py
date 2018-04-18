# Author:	Andy Horn
# Date:		4/4/2018
# Modified:	4/5/2018

# Purpose:	Create functions to test threading.

import time
from threading import Timer

################################################################################

def print_time(title='default', cycles=3, delay=1):
	for i in range(cycles):
		print(title + ": " + time.ctime(time.time()))
		time.sleep(delay)

################################################################################

def raise_alarm():
	raise TimeException

###############################################################################

def alarm(count, run):
    print("Process timed out at count %i!") % count
    del run[0] # acts like pass-by-reference, removes the only value in the list
    # essentially turning run into a False boolean.

################################################################################

def timer_test(time_to_watch=0):
    count = 0
    run = [1] # allows 'alarm' method to impact this method:
    # Python normally uses pass-by-value, but passing and modifying a list will
    # simulate passing by reference.
    while run and count < 10:
        print("Count: %i") % count
    if time_to_watch:
        timer = Timer(time_to_watch, alarm, (count, run)) # create a new timer thread:
        # this is necessary, as a timer thread can only be started once, so we
        # must create a new thread for each loop through.
        timer.start() # start the timer
    time.sleep(count) # if sleeping longer than 3 seconds, timer should call
        # the 'alarm' method above.
    if time_to_watch:
        timer.cancel() # cancel the timer to prevent false timeouts
    print("Count: %i completed.") % count
    if run:
        count += 1
    if not run:
        # if the process is killed by a timeout, success!
        print("Success! Process ended at count " + str(count)) 
   #  if count == 5:
        # otherwise, failure.
       #  print("Count reached 5")

#################################################################################
