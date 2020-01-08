# encoding=utf-8

import redis


def get_redis_handler():
    host = '192.168.2.110'
    # host = '192.168.10.10'
    port = '6379'
    db = 0

    pool = redis.ConnectionPool(host=host, port=port, db=db)
    rds = redis.Redis(connection_pool=pool)
    return rds

