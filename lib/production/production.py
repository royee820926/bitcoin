# encoding=utf-8

from lib.common import TimeOperation
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
        实盘入口
        :return:
        """
        # pandas 初始化参数
        PandasModule.init()

        # 获取当前合约数据（历史或实盘）
        # 指定合约数据类型
        instrument_id = 'BTC-USD-SWAP'
        # 获取一天的分钟K线数据
        df = cls.get_data(instrument_id)
        # 取最后一条的时间，作为后续读取的时间
        last_one = df.iloc[len(df)-1]
        last_time = last_one['candle_begin_time']
        last_timestamp = TimeOperation.string2timestamp(str(last_time), '%Y-%m-%d %H:%M:%S')

        # 添加下一分钟的数据
        df = cls.append_one_swap_from_mongo(instrument_id, df=df, start_time=(last_timestamp + 60))

        # 删除第一条数据
        cls.delete_first_one(df)
        print(df)
        exit()
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
        # 数据库起始时间 2020-01-05 13:49:00 -> 1578203340
        start_time = '2020-01-05 13:49:00'
        start_time = int(TimeOperation.string2timestamp(start_time, '%Y-%m-%d %H:%M:%S'))
        result = PandasModule.get_swap_from_mongo(instrument_id, start_time=start_time, as_df=as_df)

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


