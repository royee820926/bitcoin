# encoding=utf-8
# 计算一分钟交易数据，计算后写入MongoDB

import pandas as pd

from config.spot_coin import spot_coin_type
from config.swap_coin import swap_coin_type
from lib.db.mongo_handler import MongoHandle

import requests
from lib.okex.exceptions import OkexAPIException


##########
# 初始化 #
##########
# 成交数据汇总累计（默认5秒存储）
# ['BTC-USDT']['timestamp']
spot_total_dict = {}
swap_total_dict = {}
# 成交量汇总
# ['BTC-USDT']['timestamp']
# {
#     'buy_volume': 0,
#     'sell_volume': 0,
# }
spot_total_volume = {}
swap_total_volume = {}
# 成交量汇总数据结构
default_volume_struct = {
    'buy_volume'  : 0,
    'sell_volume' : 0,
}

# 初始化现货交易
for instrument_id in spot_coin_type:
    # 初始化DataFrame
    # trade_spot_df[instrument_id] = pd.DataFrame(columns=['timestamp', 'trade_id', 'price', 'size', 'side', 'buy_size', 'sell_size'])
    # 初始化交易数据，按一分钟时间戳分组
    spot_total_dict[instrument_id] = {}
    spot_total_volume[instrument_id] = {}


# 初始化合约交易
for instrument_id in swap_coin_type:
    # 初始化DataFrame
    # trade_swap_df[instrument_id] = pd.DataFrame(columns=['timestamp', 'trade_id', 'price', 'size', 'side', 'buy_size', 'sell_size'])
    # 初始化交易数据，按一分钟时间戳分组
    swap_total_dict[instrument_id] = {}
    swap_total_volume[instrument_id] = {}




###############################
# 测试单个
instrument_id = 'BTC-USDT'
redis_key = 'BTC-USDT-TRADE'
###############################

thread_dict = {}



