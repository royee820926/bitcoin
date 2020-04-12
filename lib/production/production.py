# encoding=utf-8

from lib.api.okex.swap_api import SwapApi
import pandas as pd
from lib.pandas_module import PandasModule
from config.swap_coin import swap_coin_type
from lib.strategy.long_position import LongPositionStrategy as lps
from lib.strategy.long_selling import LongSellingStrategy as lss

import time
from lib.pandas_module import PandasModule
from lib.db.mongo_handler import MongoHandle


class Production:
    """
    实盘生产环境
    """
    @classmethod
    def run(cls):
        """
        实盘入
        :return:
        """
        # pandas 初始化参数
        PandasModule.init()

        # 获取当前合约数据（历史或实盘）
        # 指定合约数据类型
        instrument_id = 'BTC-USD-SWAP'
        # 获取一天的分钟K线数据
        df = cls.get_data(instrument_id)

        # 重采样（5分钟采样）
        rule_type = '5T'
        df = PandasModule.resample(df=df, rule_type=rule_type)

        # 1、循环加入数据后
        # 2、产生买卖信号
        # 3、计算收益率
        while True:
            pass

        # 做多信号
        lps.boll_upward_through(df=df)

        # 做多平仓
        lss.boll_downward_through(df=df)

        print(df)
        exit()

    @classmethod
    def get_data(cls, instrument_id, as_df=True):
        # result = cls.get_data_from_api(instrument_id, as_df=as_df)
        # result = cls.get_spot_from_mongo(instrument_id, as_df=as_df)

        # 历史数据测试
        # 数据库起始时间 1578203340
        start_time = 1578203340
        result = cls.get_swap_from_mongo(instrument_id, start_time=start_time, as_df=as_df)
        print(result)
        exit()
        return result

    @classmethod
    def get_data_from_api(cls, instrument_id, as_df=True):
        """
        从API接口获取数据
        :param instrument_id: 数据类型
        :param as_df: 获取的数据是否转换成DataFrame
        :return:
        """
        result = SwapApi.get_kline_more(instrument_id)
        if as_df:
            df = pd.DataFrame(result)
            df['candle_begin_time'] = pd.to_datetime(df['candle_begin_time'], format='%Y-%m-%d %H:%M:%S')
            return df
        return result

    @classmethod
    def get_swap_from_mongo(cls, instrument_id, start_time=0, end_time=0, kline_length=2 * 24 * 60, as_df=True):
        """
        从数据库中获取合约数据（默认倒序）
        :param instrument_id:
        :param start_time: 开始时间戳
        :param end_time: 结束时间戳（下不包含）
        :param kline_length: K线数据的分钟数（默认2天）
        :param as_df: 获取结果后，是否转换成DataFrame
        :return:
        """
        result = []
        limit = 0
        time_sort = 1
        collection = MongoHandle.get_swap_collection(instrument_id)

        # 判断查询条件和返回条数
        if start_time != 0 and end_time != 0:
            condition = {"time": {"$gte": int(start_time), "$lt": int(end_time)}}
        elif start_time != 0:
            condition = {"time": {"$gte": int(start_time)}}
            limit = kline_length
        elif end_time != 0:
            condition = {"time": {"$lt": int(end_time)}}
            limit = kline_length
            time_sort = -1
        else:
            # 没有开始结束时间，则end_time为当前时间戳
            end_time = int(time.time())
            condition = {"time": {"$lt": int(end_time)}}
            limit = kline_length
            time_sort = -1

        temp = collection.find(condition).sort([('time', time_sort)])
        if limit > 0:
            temp = temp.limit(kline_length)
        # 添加结果
        for item in temp:
            result.append({
                'candle_begin_time': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(item['time'])),
                'open': float(item['open']),
                'high': float(item['high']),
                'low': float(item['low']),
                'close': float(item['close']),
                'volume': float(item['volume']),
            })
        if time_sort == -1:
            result = list(reversed(result))
        if as_df:
            df = pd.DataFrame(result)
            df['candle_begin_time'] = pd.to_datetime(df['candle_begin_time'], format='%Y-%m-%d %H:%M:%S')
            return df
        return result

    @classmethod
    def append_data(cls, df, ):
        """
        追加数据
        :param df:
        :return:
        """
        pass

