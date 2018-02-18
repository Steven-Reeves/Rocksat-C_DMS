# Object oriented implementation of DMS
# Steven Reeves
# RockSat-C Software Engineering Lead
# 2/11/2018

import time
import csv
from datetime import datetime


class DataWriter:
    def __init__(self, colNames, fname):
        # May not need columns
        # self.columns = len(colNames)
        colNames.insert(0, "Time")
        self.myArray = colNames
        self.filename = fname
        csvfile = open(self.filename + ".csv", "a")
        self.writer = csv.writer(csvfile)
        self.writer.writerow(self.myArray)

    def writeTo(self, myList):
        time_array = [str(datetime.now())]
        time_array.extend(myList)
        self.writer.writerow(time_array)


def experiment_factory(experiment_name):
    try:
        # check directories for class files. Users can add them manually!
        if experiment_name == 'TestExp':
            instance = TestExperiment('TestExp')
        else:
            instance = 0
    except():
        raise ImportError('{} is not a valid experiment')
    return instance


class TestExperiment:
    def __init__(self, ename):
        # Is name needed?
        self.name = ename
        self.com = Communicator()
        self.columns = ["height", "speed", "Other idea", "last check"]
        self.dataWriter = DataWriter(self.columns, "Test")


class Communicator:
    def __init__(self):
        self.isConnected = False


myExperiment = experiment_factory('Test4Exp')

myData = ["Some", "cool", "Data", "here!"]
myExperiment.dataWriter.writeTo(myData)
myData = ["653", "659", "666", "9636"]
myExperiment.dataWriter.writeTo(myData)
myData = ["what", "Is", "going", "on"]
myExperiment.dataWriter.writeTo(myData)
myData = ["nice", "noep", "eh", "*/--89+4!"]
myExperiment.dataWriter.writeTo(myData)
myData = ["more", "234526", "vvv", "!@#%&*(!"]
myExperiment.dataWriter.writeTo(myData)

'''
print("Initating fake data")
colList = ["height", "speed", "Other idea", "last check"]

print("opening new DataWriter")
myDW = DataWriter(colList, "testDW")

myList = ["Some", "cool", "Data", "here!"]
myDW.writeTo(myList)
myList = ["Different", "stuff", "here!", "wooo"]
myDW.writeTo(myList)
'''