import storm
import redis


class TopNStoreBolt(storm.BasicBolt):
    # Initialize this instance
    def initialize(self, conf, context):
        # redis configuration converted into a dictonary
        self._redis = conf.get("redis")
        storm.logInfo("Top N Store bolt instance starting...")

        # TODO
        # Connect to Redis using redis.Redis() with redis configuration in self._redis dictionary
        # Hint: Add necessary instance variables and classes if needed
        self.r = redis.Redis(host=self._redis["host"], socket_timeout=self._redis["timeout"], port=6379, db=0,
                             password="uiuc_cs498_mp11")

    def process(self, tup):
        # TODO
        # Task: save the top-N word to redis under the specified hash name
        self.r.hset(self._redis["hashKey"], "top-N", str(tup.values[1]))
        # End


# Start the bolt when it's invoked
TopNStoreBolt().run()
