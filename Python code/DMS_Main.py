# Object oriented implementation of DMS
# Steven Reeves
# RockSat-C Software Engineering Lead
# 2/11/2018

import time
import csv
from datetime import datetime

class DataWriter:
    def __init__(self, colNames, fname):
        self.columns = len(colNames)
        colNames.insert(0, "Time")
        self.myArray = []
        self.myArray.append(colNames)
        self.filename = fname
    def writeTo(self, myList):
        timeArray = [str(datetime.now())]
        timeArray.extend(myList)
        self.myArray.append(timeArray)
        with open(self.filename + ".csv", "a") as d:
            writer = csv.writer(d)
            # TODO: writer object writing whole array out every time. Memory issue with big array?
            writer.writerows(self.myArray)

print("Initating fake data")
colList = ["height", "speed", "Other idea", "last check"]

print("opening new DataWriter")
myDW = DataWriter(colList, "testDW")

myList = ["Some", "cool", "Data", "here!"]
myDW.writeTo(myList)
myList = ["Different", "stuff", "here!", "wooo"]
myDW.writeTo(myList)
