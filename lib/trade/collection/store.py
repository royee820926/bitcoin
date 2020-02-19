# encoding=utf-8

from config.spot_coin import spot_coin_type
from config.swap_coin import swap_coin_type


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

