# encoding=utf-8

import threading
from lib.api.okex.spot_api import SpotApi
from lib.api.okex.swap_api import SwapApi
from lib.common import get_dict, TimeOption
from config.spot_coin import spot_coin_type
from config.swap_coin import swap_coin_type


class TradesThread(threading.Thread):
    """
    成交数据采集，并入库
    """
    __trade_type = ''

    def __init__(self, thread_id, coin_name, trade_type):
        threading.Thread.__init__(self)
        self.threadID = thread_id
        self.name = coin_name
        self.__trade_type = trade_type

    def get_trade_type(self):
        """
        交易类别 spot | swap
        :return:
        """
        return self.__trade_type

    def run(self):
        """
        线程入口
        :return:
        """
        while True:
            # 获取交易记录
            trade_list = SpotApi.get_trades(self.getName())

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


class VolumeStore:
    """
    成交量数据汇总
    """
    # 成交量数据结构
    default_dict_struct = {
        'buy_volume': 0,
        'sell_volume': 0,
        'trade_ids': [],
    }
    # 成交量汇总数据结构
    default_volume_struct = {
        'buy_volume'  : 0,
        'sell_volume' : 0,
    }
    # 5秒成交数据结构
    __total_dict = {}
    # 1分钟成交数据汇总
    __total_volume = {}

    @classmethod
    def init_store(cls):
        """
        初始化现货交易
        :return:
        """
        # 初始化现货交易
        for coin_name in spot_coin_type:
            # 初始化DataFrame
            # trade_spot_df[coin_name] = pd.DataFrame(columns=['timestamp', 'trade_id', 'price', 'size', 'side', 'buy_size', 'sell_size'])
            # 初始化交易数据，按一分钟时间戳分组
            cls.__total_dict[coin_name] = {}
            cls.__total_volume[coin_name] = {}

        # 初始化合约交易
        for coin_name in swap_coin_type:
            # 初始化DataFrame
            # trade_swap_df[coin_name] = pd.DataFrame(columns=['timestamp', 'trade_id', 'price', 'size', 'side', 'buy_size', 'sell_size'])
            # 初始化交易数据，按一分钟时间戳分组
            cls.__total_dict[coin_name] = {}
            cls.__total_volume[coin_name] = {}

    @classmethod
    def get_dict(cls, coin_name):
        """
        5秒成交数据结构
        :param coin_name:
        :return:
        """
        if coin_name in cls.__total_dict:
            return cls.__total_dict[coin_name]
        return None

    @classmethod
    def get_volume(cls, coin_name):
        """
        1分钟成交数据汇总
        :param coin_name:
        :return:
        """
        if coin_name in cls.__total_volume:
            return cls.__total_volume[coin_name]
        return None

    @classmethod
    def init_dict_timestamp(cls, coin_name, timestamp):
        """
        初始化 成交量数据结构
        total_dict[coin_name][base_timestamp] = data
        :param coin_name:
        :param timestamp:
        :param data:
        :return:
        """
        cls.__total_dict[coin_name][timestamp] = cls.default_dict_struct

    @classmethod
    def init_volume_timestamp(cls, coin_name, timestamp):
        """
        初始化 成交量数据结构
        total_dict[coin_name][base_timestamp] = data
        :param coin_name:
        :param timestamp:
        :param data:
        :return:
        """
        cls.__total_volume[coin_name][timestamp] = cls.default_volume_struct

    @classmethod
    def dict_append_trade_id(cls, coin_name, timestamp, trade_id):
        """
        成交量数据结构 添加 trade_id
        :param coin_name:
        :param timestamp:
        :param trade_id:
        :return:
        """
        cls.__total_dict[coin_name][timestamp]['trade_ids'].append(trade_id)

    @classmethod
    def dict_add_buy_volume(cls, coin_name, timestamp, volume):
        """
        成交量数据结构 添加买入成交量
        :param coin_name:
        :param timestamp:
        :param volume:
        :return:
        """
        cls.__total_dict[coin_name][timestamp]['buy_volume'] += volume

    @classmethod
    def dict_add_sell_volume(cls, coin_name, timestamp, volume):
        """
        成交量数据结构 添加卖出成交量
        :param coin_name:
        :param timestamp:
        :param volume:
        :return:
        """
        cls.__total_dict[coin_name][timestamp]['sell_volume'] += volume

    @classmethod
    def volume_add_buy_volume(cls, coin_name, timestamp, volume):
        """
        成交量数据结构 添加买入成交量
        :param coin_name:
        :param timestamp:
        :param volume:
        :return:
        """
        cls.__total_volume[coin_name][timestamp]['buy_volume'] += volume

    @classmethod
    def volume_add_sell_volume(cls, coin_name, timestamp, volume):
        """
        成交量数据结构 添加卖出成交量
        :param coin_name:
        :param timestamp:
        :param volume:
        :return:
        """
        cls.__total_volume[coin_name][timestamp]['sell_volume'] += volume

    @classmethod
    def is_in_dict_timestamp(cls, coin_name, timestamp):
        if timestamp in cls.__total_dict[coin_name]:
            return True
        return False

    @classmethod
    def is_in_volume_timestamp(cls, coin_name, timestamp):
        if timestamp in cls.__total_volume[coin_name]:
            return True
        return False

    @classmethod
    def get_dict_timestamp_list(cls, coin_name):
        """
        获取币种下的不同时间戳的成交量列表
        :param coin_name:
        :return:
        """
        return cls.__total_dict[coin_name]

    @classmethod
    def get_volume_timestamp_list(cls, coin_name):
        """
        获取币种下的不同时间戳的成交量列表
        :param coin_name:
        :return:
        """
        return cls.__total_volume[coin_name]

