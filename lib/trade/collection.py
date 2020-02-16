# encoding=utf-8

import threading
from lib.api.okex.spot_api import SpotApi
from lib.api.okex.swap_api import SwapApi
from lib.common import get_dict, TimeOption
from config.spot_coin import spot_coin_type
from config.swap_coin import swap_coin_type


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


class TradesThread(threading.Thread):


    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def __init_total(self):


    def run(self):
        """
        线程入口
        :return:
        """
        while True:
            # 获取交易记录
            trade_list = SpotApi.get_trades(instrument_id)

            # 交易记录条数
            trade_len = len(trade_list)
            # 遍历交易记录，倒序读取
            for index in range(trade_len - 1, 0, -1):
                item = trade_list[index]
                # ISO8601 时间转换
                # 转成北京时间
                format_str = '%Y-%m-%dT%H:%M:%S.%fZ'
                time_array = TimeOption.string2datetime(item['timestamp'], format_str, hours=8)
                # 基准时间秒数（以5秒为单位的时间起点的时间戳）
                tm_second = time_array.second
                # 基准秒数（以基准秒数转换后的时间戳作为列表索引）
                temp = tm_second % 5
                base_second = tm_second - temp
                # 分钟整点的datetime
                minute_array = TimeOption.set_datetime(time_array, second=0)
                # 设置基准秒数
                time_array = TimeOption.set_datetime(time_array, second=base_second)
                # 设置基准时间戳
                base_timestamp = TimeOption.datetime2timestamp(time_array)

                trade_id = item['trade_id']
                price = float(item['price'])
                size = float(item['size'])
                volume = price * size
                # buy: 买入; sell: 卖出
                side = item['side']

                # 检查trade_id 是否在前一个5秒插入过
                # 如果插入过，则略过
                item = get_dict(spot_total_dict, instrument_id, base_timestamp)

                data = {
                    'buy_volume': 0,
                    'sell_volume': 0,
                    'trade_ids': [],
                }

                item = get_dict(spot_total_dict, instrument_id, base_timestamp)

                if item is None:
                    spot_total_dict[instrument_id][base_timestamp] = data
                else:
                    if trade_id in item['trade_ids']:
                        # 如果trade_id在列表中，则跳过本次循环
                        continue

                # 添加trade_id，避免重复录入
                spot_total_dict[instrument_id][base_timestamp]['trade_ids'].append(trade_id)
                # 累加买卖交易量
                if side == 'buy':
                    spot_total_dict[instrument_id][base_timestamp]['buy_volume'] += volume
                elif side == 'sell':
                    spot_total_dict[instrument_id][base_timestamp]['sell_volume'] += volume

                ##################################################################
                # 一分钟交易量汇总到spot_total_volume | swap_total_volume，准备入库 #
                ##################################################################
                base_minute_time = TimeOption.datetime2timestamp(minute_array)
                # 初始化
                if base_minute_time not in spot_total_volume[instrument_id]:
                    spot_total_volume[instrument_id][base_minute_time] = default_volume_struct
                if side == 'buy':
                    spot_total_volume[instrument_id][base_minute_time]['buy_volume'] += volume
                elif side == 'sell':
                    spot_total_volume[instrument_id][base_minute_time]['sell_volume'] += volume

