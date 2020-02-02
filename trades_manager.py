# encoding=utf-8
# 交易数据写入pandas

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


class TradesThread(threading.Thread):
    pass


# 交易数据汇总存储（默认5秒存储）
spot_total_dict = {}
swap_total_dict = {}
last_trade_id = ''

total_default = {
    'timestamp': '',
    'trade_id': '',
    'price': 0,
    'size': 0,
    'side': '',
    'status': 0,    # 状态【0：未初始化；1：使用中】
}

# 现货交易key
for instrument_id in spot_coin_type:
    # 初始化DataFrame
    # trade_spot_df[instrument_id] = pd.DataFrame(columns=['timestamp', 'trade_id', 'price', 'size', 'side', 'buy_size', 'sell_size'])
    # 初始化交易数据
    spot_total_dict[instrument_id] = total_default

# 合约交易key
for instrument_id in swap_coin_type:
    # 初始化DataFrame
    # trade_swap_df[instrument_id] = pd.DataFrame(columns=['timestamp', 'trade_id', 'price', 'size', 'side', 'buy_size', 'sell_size'])
    swap_total_dict[instrument_id] = total_default

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
    # 遍历交易记录
    for index in range(trade_len - 1, 0, -1):
        item = trade_list[index]
        last_trade_id = item['trade_id']
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

        data = {
            'timestamp': base_timestamp,
            'trade_id' : item['trade_id'],
            'price': float(item['price']),
            'size': float(item['size']),
            'side': item['side'],
        }
        # 添加一条pandas数据
        # trade_spot_df[redis_key] = trade_spot_df[redis_key].append(temp, ignore_index=True)

    exit()

