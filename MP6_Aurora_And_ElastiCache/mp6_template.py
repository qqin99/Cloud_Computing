import json
import sys
import logging
import redis
import pymysql
import requests

DB_HOST = "database-mp6.cluster-ci8t0zsas9xb.us-east-1.rds.amazonaws.com"
DB_USER = "admin"
DB_PASS = "4658163Qq"
DB_NAME = "mp6heros"
DB_TABLE = "heros"
REDIS_URL = "redis://mp6-redis.qaqlpu.ng.0001.use1.cache.amazonaws.com:6379"
# Database = DB(host=DB_HOST, user=DB_USER, password = DB_PASS, db =DB_NAME)

TTL = 10


class DB:
    def __init__(self, **params):
        params.setdefault("charset", "utf8mb4")
        params.setdefault("cursorclass", pymysql.cursors.DictCursor)

        self.mysql = pymysql.connect(**params)

    def query(self, sql):
        with self.mysql.cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchall()

    def get_idx(self, table_name):
        with self.mysql.cursor() as cursor:
            cursor.execute(f"SELECT MAX(id) as id FROM {table_name}")
            idx = str(cursor.fetchone()['id'] + 1)
            return idx

    def insert(self, idx, data):
        with self.mysql.cursor() as cursor:
            hero = data["hero"]
            power = data["power"]
            name = data["name"]
            xp = data["xp"]
            color = data["color"]

            sql = f"INSERT INTO heros (`id`, `hero`, `power`, `name`, `xp`, `color`) VALUES ('{idx}', '{hero}', '{power}', '{name}', '{xp}', '{color}')"

            cursor.execute(sql)
            self.mysql.commit()


def read(use_cache, indices, Database, Cache):
    """Retrieve records from the cache, or else from the database."""
    res = []
    for num in indices:
        sql = f"select * from heros where id = '{num}'"

        if use_cache:
            # result = json.loads(Cache.get(str(num)))
            result = Cache.get(str(num))
            # cache hit:
            if result:
                # use decode() on the Cache reads
                res.append(json.loads(result))
            # cache miss
            else:
                result = Database.query(sql)
                Cache.setex(str(num), TTL, json.dumps(result[0]))
                res.append(result[0])
        else:
            result = Database.query(sql)
            res.append(result[0])
    # res = [item for sublist in res for item in sublist]
    return res


def write(use_cache, sqls, Database, Cache):
    # write through strategy
    if use_cache:
        for sql in sqls:
            id = Database.get_idx('heros')
            Database.insert(int(id), sql)
            sql["id"] = id
            Cache.setex(id, TTL, json.dumps(sql))
    else:
        for sql in sqls:
            id = Database.get_idx('heros')
            Database.insert(int(id), sql)


def lambda_handler(event, context):
    USE_CACHE = (event['USE_CACHE'] == "True")
    REQUEST = event['REQUEST']

    # initialize database and cache
    try:
        Database = DB(host=DB_HOST, user=DB_USER, password=DB_PASS, db=DB_NAME)
    except pymysql.MySQLError as e:
        print("ERROR: Unexpected error: Could not connect to MySQL instance.")
        print(e)
        sys.exit()

    Cache = redis.Redis.from_url(REDIS_URL)

    result = []
    if REQUEST == "read":
        # event["SQLS"] should be a list of integers eg [1,2,3]
        result = read(USE_CACHE, event["SQLS"], Database, Cache)

    elif REQUEST == "write":
        # event["SQLS"] should be a list of jsons
        write(USE_CACHE, event["SQLS"], Database, Cache)
        result = "write success"

    return {
        'statusCode': 200,
        'body': result
    }
