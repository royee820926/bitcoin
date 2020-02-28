# encoding=utf-8

import threading
from config.spot_coin import spot_coin_type
from config.swap_coin import swap_coin_type


class VolumeStore:
    """
    成交量数据汇总存储
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
        'trade_ids': [],
    }
    # 5秒成交数据结构
    __total_dict = {}
    # 1分钟成交数据汇总
    __total_volume = {}
    # 成交量数据操作锁
    __volume_lock = threading.Lock()

    @classmethod
    def get_lock(cls):
        return cls.__volume_lock

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
    def get_total_dict(cls):
        """
        获取全部的5秒数据
        :return:
        """
        return cls.__total_dict

    @classmethod
    def get_total_volume(cls):
        """
        获取全部的1分钟数据
        :return:
        """
        return cls.__total_volume

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
    def volume_set_volume(cls, coin_name, timestamp, buy_volume=0, sell_volume=0, symbol=''):
        """
        设置成交量（+ 增加；- 减少；0 清空）
        :param coin_name:
        :param timestamp:
        :param buy_volume:
        :param sell_volume:
        :param symbol:
        :return: 返回修改前的数据
        """
        result = cls.__total_volume[coin_name][timestamp]
        if symbol == '+':
            cls.volume_add_buy_volume(coin_name, timestamp, buy_volume)
            cls.volume_add_sell_volume(coin_name, timestamp, sell_volume)
        elif symbol == '0':
            cls.__total_volume[coin_name][timestamp]['buy_volume'] = 0
            cls.__total_volume[coin_name][timestamp]['sell_volume'] = 0
        return result

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
    def del_volume_by_timestamp(cls, coin_name, timestamp):
        """
        删除时间戳对应的成交量数据
        :param coin_name:
        :param timestamp:
        :return:
        """
        if timestamp in cls.__total_volume[coin_name]:
            cls.__total_volume[coin_name].pop(timestamp)
            return True
        return False

    @classmethod
    def is_timestamp_in_dict(cls, coin_name, timestamp):
        """
        dict中是否存在timestamp
        :param coin_name:
        :param timestamp:
        :return:
        """
        if timestamp in cls.__total_dict[coin_name]:
            return True
        return False

    @classmethod
    def is_timestamp_in_volume(cls, coin_name, timestamp):
        """
        volume中是否存在timestamp
        :param coin_name:
        :param timestamp:
        :return:
        """
        if timestamp in cls.__total_volume[coin_name]:
            return True
        return False

    @classmethod
    def get_dict_one_timestamp(cls, coin_name, timestamp):
        """
        获取单个时间戳下的成交量数据
        :param coin_name:
        :param timestamp:
        :return:
        """
        time_list = cls.get_dict(coin_name)
        if time_list is not None or timestamp in time_list:
            return time_list[timestamp]
        return None

    @classmethod
    def get_volume_one_timestamp(cls, coin_name, timestamp):
        """
        获取单个时间戳下的成交量数据
        :param coin_name:
        :param timestamp:
        :return:
        """
        time_list = cls.get_volume(coin_name)
        if time_list is not None or timestamp in time_list:
            return time_list[timestamp]
        return None
