import storm
import redis

class WordCountStoreBolt(storm.BasicBolt):
    # Initialize this instance
    def initialize(self, conf, context):
        self._redis = conf.get("redis")  # redis configuration converted into a dictonary
        # self._context = context
        storm.logInfo("Word Count Store bolt instance starting...")

        # TODO
        # Connect to Redis using redis.Redis() with redis configuration in self._redis dictionary
        # Hint: Add necessary instance variables and classes if needed
        self.r = redis.Redis(host=self._redis["host"], socket_timeout=self._redis["timeout"], port= 6379, db= 0, password= "uiuc_cs498_mp11") #, timeout= 2000
        # host ="localhost" is hard coded, self._redis can grab current host if auto-grader changed it
      # redis hash key for part A is "partAWordCount"


    def process(self, tup):
        # TODO 
        # Task: save word count pair to redis under the specified hash name
        self.r.hset(self._redis["hashKey"], tup.values[0], tup.values[1])

# Start the bolt when it's invoked
WordCountStoreBolt().run()
