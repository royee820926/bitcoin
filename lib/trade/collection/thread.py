# encoding=utf-8

import threading
import time
from lib.api.okex.spot_api import SpotApi
from lib.api.okex.swap_api import SwapApi
from lib.common import get_dict, TimeOption


class TradesThread(threading.Thread):
    """
    成交数据采集，并入库
    """
    __trade_type = ''

    def __init__(self, thread_id, coin_name, trade_type):
        threading.Thread.__init__(self)
        self.threadID = thread_id
        self.name = coin_name
        self.set_trade_type(trade_type)

    def set_trade_type(self, trade_type):
        """
        设置交易类别 spot | swap
        :param trade_type:
        :return:
        """
        self.__trade_type = trade_type

    def get_trade_type(self):
        """
        交易类别 spot | swap
        :return:
        """
        return self.__trade_type

    def get_api_trades(self):
        trade_type = self.get_trade_type()
        flag = True
        if trade_type == 'spot':
            data = SpotApi.get_trades(self.getName())
        elif trade_type == 'swap':
            data = SwapApi.get_trades(self.getName())
        else:
            data = None
            flag = False
        return data, flag

    def run(self):
        """
        线程入口
        :return:
        """
        while True:
            # 获取交易记录
            trade_list, flag = self.get_api_trades()
            if not flag:
                return
            if trade_list is None:
                continue

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
                item = get_dict(VolumeStore.get_dict(self.getName()), self.getName(), base_timestamp)

                if item is None:
                    VolumeStore.init_dict_timestamp(self.getName(), base_timestamp)
                else:
                    if trade_id in item['trade_ids']:
                        # 如果trade_id在列表中，则跳过本次循环
                        continue

                # 添加trade_id，避免重复录入
                VolumeStore.dict_append_trade_id(self.getName(), base_timestamp, trade_id)
                # 累加买卖交易量
                if side == 'buy':
                    VolumeStore.dict_add_buy_volume(self.getName(), base_timestamp, volume)
                elif side == 'sell':
                    VolumeStore.dict_add_sell_volume(self.getName(), base_timestamp, volume)

                #########################################
                # 一分钟交易量汇总到total_volume，准备入库 #
                #########################################
                base_minute_time = TimeOption.datetime2timestamp(minute_array)
                # 初始化
                if not VolumeStore.is_in_volume_timestamp(self.getName(), base_minute_time):
                    VolumeStore.init_volume_timestamp(self.getName(), base_minute_time)
                if side == 'buy':
                    VolumeStore.volume_add_buy_volume(self.getName(), base_minute_time, volume)
                elif side == 'sell':
                    VolumeStore.volume_add_sell_volume(self.getName(), base_minute_time, volume)

            # 等待500毫秒
            time.sleep(0.5)

