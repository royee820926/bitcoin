# encoding=utf-8
# 成交数据写入redis，区分买入、卖出

from lib.api.okex.spot_api import SpotApi
from lib.api.okex.swap_api import SwapApi
from config.spot_coin import spot_redis_keys
from config.swap_coin import swap_redis_keys
from lib.db.redis_handler import get_redis_handler
from lib.okex.exceptions import OkexAPIException
import time
import json
import threading
import requests

# redis = get_redis_handler()
# instrument_id = 'BTC-USDT'
#
# result = SpotApi.get_trades(instrument_id)
# result = reversed(result)
#
# for item in result:
#     item_str = json.dumps(item)
#     redis.lpush('BTC-USDT-TRADE', item_str)


class TradeToRedisThread(threading.Thread):

    def __init__(self, threadID, name, trade_type):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.trade_type = trade_type

    def run(self):
        # 获取trade接口数据
        if self.trade_type == 'spot':
            # 现货api
            SpotApi.get_trades()
        elif self.trade_type == 'swap':
            # 合约api
            pass


# 所有币线程
thread_dict = {}
thread_index = 0

# 队列键名的集合

# 初始化现货交易队列
for queue_key in spot_redis_keys:
    thread_index += 1
    trade_type = 'spot'
    thread_dict[queue_key] = TradeToRedisThread(thread_index, queue_key, trade_type)
    thread_dict[queue_key].setDaemon(True)
    thread_dict[queue_key].start()
# 初始化合约交易队列
for queue_key in swap_redis_keys:
    thread_index += 1
    trade_type = 'swap'
    thread_dict[queue_key] = TradeToRedisThread(thread_index, queue_key, trade_type)
    thread_dict[queue_key].setDaemon(True)
    thread_dict[queue_key].start()

# 阻塞线程
for qk in spot_redis_keys:
    thread_dict[qk].join()
for qk in swap_redis_keys:
    thread_dict[qk].join()

print('主线程退出')
