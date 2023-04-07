import heapq
from collections import Counter

import storm


class TopNFinderBolt(storm.BasicBolt):
    # Initialize this instance
    def initialize(self, conf, context):
        self._conf = conf
        self._context = context

        storm.logInfo("Counter bolt instance starting...")

        # TODO:
        # Task: set N
        # Create a new counter for this instance
        self._N = self._conf["N"]

        self._listOfCounts= []
        self._listOfWords = []
        # End

        # Hint: Add necessary instance variables and classes if needed

    def process(self, tup):
        '''
        TODO:
        Task: keep track of the top N words
        Hint: implement efficient algorithm so that it won't be shutdown before task finished
              the algorithm we used when we developed the auto-grader is maintaining a N size min-heap
        '''
        # Get the word from the inbound tuple
        word = tup.values[0]
        cnt = tup.values[1]
        if len(self._listOfCounts) < self._N and word not in self._listOfWords:
            self._listOfWords.append(word)
            self._listOfCounts.append(cnt)

        else:
            if word not in self._listOfWords:
                least = min(self._listOfCounts)
                if cnt>=least:
                    index = self._listOfCounts.index(least)
                    self._listOfWords[index] = word
                    self._listOfCounts[index] = cnt
                output= ''
                for item in self._listOfWords:
                    output = output + ', ' + item
                output = output.split(", ", 1)[1]

                storm.logInfo("Emitting %s" %output)
                # Emit the word and count
                topN = "top-N"
                storm.emit([topN,output])
        # End


# Start the bolt when it's invoked
TopNFinderBolt().run()
