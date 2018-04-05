# Author:	Andy Horn
# Date:		4/4/2018
# Modified:	4/4/2018

# Purpose:	Create functions to test threading.

import time
import datetime

def print_time(title='default', cycles=3, delay=1):
	for i in range(cycles):
		print(title + ": " + time.ctime(time.time()))
		time.sleep(delay)
