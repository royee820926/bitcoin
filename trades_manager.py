# encoding=utf-8
# 计算一分钟交易数据，计算后写入MongoDB

import time
import datetime
import pandas as pd
from lib.api.okex.spot_api import SpotApi
from lib.api.okex.swap_api import SwapApi
from config.spot_coin import spot_coin_type
from config.swap_coin import swap_coin_type
from lib.db.mongo_handler import get_spot_collection, get_swap_collection
import threading
import requests
from lib.okex.exceptions import OkexAPIException
from lib.common import get_dict

##########
# 初始化 #
##########
# 交易数据汇总存储（默认5秒存储）
spot_total_dict = {}
spot_last_trade_id_dict = {}
swap_total_dict = {}
swap_last_trade_id_dict = {}

# 现货交易key
for instrument_id in spot_coin_type:
    # 初始化DataFrame
    # trade_spot_df[instrument_id] = pd.DataFrame(columns=['timestamp', 'trade_id', 'price', 'size', 'side', 'buy_size', 'sell_size'])
    # 初始化交易数据，按一分钟时间戳分组
    spot_total_dict[instrument_id] = {}
    spot_last_trade_id_dict[instrument_id] = ''

# 合约交易key
for instrument_id in swap_coin_type:
    # 初始化DataFrame
    # trade_swap_df[instrument_id] = pd.DataFrame(columns=['timestamp', 'trade_id', 'price', 'size', 'side', 'buy_size', 'sell_size'])
    # 初始化交易数据，按一分钟时间戳分组
    swap_total_dict[instrument_id] = {}
    swap_last_trade_id_dict[instrument_id] = ''


class TradesThread(threading.Thread):
    pass


###############################
instrument_id = 'BTC-USDT'
redis_key = 'BTC-USDT-TRADE'
###############################
while True:
    # 获取交易记录
    try:
        trade_list = SpotApi.get_trades(instrument_id)
    except requests.exceptions.SSLError as rse:
        # 请求错误
        print(rse)
        print('requests.exceptions.SSLError')
        exit()

    except requests.exceptions.ConnectionError as rce:
        # 由于连接方在一段时间后没有正确答复或连接的主机没有反应，连接尝试失败。
        print(rce)
        print('requests.exceptions.ConnectionError')
        exit()

    except requests.exceptions.ReadTimeout as rto:
        # 读请求超时
        print(rto)
        print('requests.exceptions.ReadTimeout')
        exit()

    except requests.exceptions.ConnectTimeout as cto:
        # 连接请求超时
        print(cto)
        print('requests.exceptions.ConnectTimeout')
        exit()

    except OkexAPIException as oae:
        print(oae)
        print('OkexAPIException')
        exit()

    # 交易记录条数
    trade_len = len(trade_list)
    # 遍历交易记录，倒序读取
    for index in range(trade_len - 1, 0, -1):
        item = trade_list[index]
        # ISO8601 时间转换
        time_array = datetime.datetime.strptime(item['timestamp'], '%Y-%m-%dT%H:%M:%S.%fZ')
        # 转成北京时间
        time_array = time_array + datetime.timedelta(hours=8)
        # 时间戳
        timestamp = time.mktime(time_array.timetuple())
        # 基准时间秒数（以5秒为单位的时间起点的时间戳）
        tm_second   = time_array.second
        # 基准秒数（以基准秒数转换后的时间戳作为列表索引）
        temp = tm_second % 5
        base_second = tm_second - temp
        # 设置基准秒数
        time_array = time_array.replace(second=base_second)

        # 设置基准时间戳
        base_timestamp = time.mktime(time_array.timetuple())
        trade_id = item['trade_id']
        price = float(item['price'])
        size = float(item['size'])
        volume = price * size
        # buy: 买入; sell: 卖出
        side = item['side']

        data = {
            'buy_volume': 0,
            'sell_volume': 0,
            'trade_ids': [],
        }

        item = get_dict(spot_total_dict, instrument_id, base_timestamp)
        if item is None:
            spot_total_dict[instrument_id][base_timestamp] = data
        # 添加trade_id，避免重复录入
        spot_total_dict[instrument_id][base_timestamp]['trade_ids'].append(trade_id)
        # 累加买卖交易量
        if side == 'buy':
            spot_total_dict[instrument_id][base_timestamp]['buy_volume'] += volume
        elif side == 'sell':
            spot_total_dict[instrument_id][base_timestamp]['sell_volume'] += volume

    # 记录instrument_id对于的币
    spot_last_trade_id_dict[instrument_id] = trade_id


    print(spot_total_dict[instrument_id])
    exit()

