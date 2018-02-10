# initial sandbox for writing to and from stuff
# \ characters not working
import time
import csv
from datetime import datetime


print("Hello!")



log = open("log.txt", "w")

log.write("*************Initating log*****************\n")
log.write(str(datetime.now())+ "\n")
log.write("Looping to create data in two dimensional array\n")
myData = [["Time", "Count", "Col 3", "Col 4"]]

for x in range(1,10):
    myData.append([str(datetime.now()),x,"filler","example"])
    log.write("Data Written!\n")
    time.sleep(1)   

log.write("Fake data initialized\n")
log.write("This is where to start a .csv file\n")
with open("data.csv", "w") as d:
    writer = csv.writer(d)
    writer.writerows(myData)

log.write("Data written to .csv!\n")

print("Closing log")
log.close()



      
