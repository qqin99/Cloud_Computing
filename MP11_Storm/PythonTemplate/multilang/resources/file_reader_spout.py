# import os
# from os.path import join

from time import sleep
import time
# from streamparse import Spout
import storm


class FileReaderSpout(storm.Spout):

    def initialize(self, conf, context):
        self._conf = conf
        self._context = context
        self._complete = False

        storm.logInfo("Spout instance starting...")

        # TODO:
        # Task: Initialize the file reader
        # hint: get the filename from conf argument
        self._f = open(self._conf["infile"], "r")  # "/tmp/data.txt"
        # End

    def nextTuple(self):
        # TODO:
        # Task 1: read the next line and emit a tuple for it
        line = self._f.readline()
        if  len(line) == 0:
            self._complete = True
            time.sleep(1)

        if self._complete == False:
            sentence = line.lstrip().rstrip()
        # Task 2: don't forget to sleep for 1 second when the file is entirely read to prevent a busy-loop
            storm.logInfo("Emitting %s" % sentence)
            storm.emit([sentence])
        # End


# Start the spout when it's invoked
FileReaderSpout().run()
