# encoding=utf-8
# 计算一分钟交易数据，计算后写入MongoDB

import pandas as pd

from config.spot_coin import spot_coin_type
from config.swap_coin import swap_coin_type
from lib.trade.collection.thread.coin_thread import CoinThread
from lib.trade.collection.thread.coin_store_thread import CoinStoreThread
from lib.trade.collection.volume_store import VolumeStore


###############################
# 测试单个
# instrument_id = 'BTC-USDT'
spot_coin_type = ['BTC-USDT']
###############################

# 初始化store
VolumeStore.init_store()
thread_dict = {}
thread_index = 0

# 成交量采集线程 启动
trade_type = 'spot'
for coin_name in spot_coin_type:
    thread_index += 1
    thread_dict[coin_name] = CoinThread(thread_index, coin_name, trade_type)
    # 设置守护线程
    thread_dict[coin_name].setDaemon(True)
    # 启动线程
    thread_dict[coin_name].start()
    print('启动线程: %d, 名字: %s' % (thread_index, coin_name))

# trade_type = 'swap'
# for coin_name in swap_coin_type:
#     thread_index += 1
#     thread_dict[coin_name] = CoinThread(thread_index, coin_name, trade_type)
#     # 设置守护线程
#     thread_dict[coin_name].setDaemon(True)
#     # 启动线程
#     thread_dict[coin_name].start()
#     print('启动线程: %d, 名字: %s' % (thread_index, coin_name))

print('===================================')


# 入库、统计线程启动
thread_index += 1
coin_store_thread = CoinStoreThread(thread_index, 'coin_store_thread')
coin_store_thread.setDaemon(True)
coin_store_thread.start()


# 阻塞线程
for coin_name, coin_thread in thread_dict.items():
    coin_thread.join()
coin_store_thread.join()


print('主线程退出')
