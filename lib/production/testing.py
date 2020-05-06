# encoding=utf-8

from lib.common import TimeOperation
from lib.api.okex.swap_api import SwapApi
import pandas as pd
from lib.pandas_module import PandasModule
from config.swap_coin import swap_coin_type
from lib.strategy.long_position import LongPositionStrategy as lps
from lib.strategy.long_selling import LongSellingStrategy as lss

from lib.pandas_module import PandasModule
from lib.indicator.rsi_indicator import RsiIndicator


class Testing:
    """
    实盘生产环境
    """
    @classmethod
    def run(cls):
        """
        模拟实盘
        :return:
        """
        # pandas 初始化参数
        PandasModule.init()

        # 获取当前合约数据（历史或实盘）
        # 指定合约数据类型
        instrument_id = 'BCH-USD-SWAP'
        # 获取一天的分钟K线数据
        df = cls.get_data(instrument_id)

        # 取最后一条的时间，作为后续读取的时间
        last_one = df.iloc[len(df)-1]
        last_time = last_one['candle_begin_time']
        # 时间戳
        last_timestamp = TimeOperation.string2timestamp(str(last_time), '%Y-%m-%d %H:%M:%S')
        next_timestamp = last_timestamp + 60

        # # 添加下一分钟的数据
        # df = cls.append_one_swap_from_mongo(instrument_id, df=df, start_time=next_timestamp)
        # # 删除第一条数据
        # cls.delete_first_one(df)

        # 1、数据重采样
        # 2、产生买卖信号，判断趋势等关键属性
        # 3、计算收益率
        # 4、追加新的K线数据，删除第一条K线数据
        while True:
            # 重采样（5分钟采样）
            rule_type = '5T'
            df5t = PandasModule.resample(df=df, rule_type=rule_type)

            # 产生交易信号
            # RSI6
            RsiIndicator.get_value(df=df5t, rsi_name='rsi6')
            # 去除rsi开头的空行
            df5t.dropna(axis=0, how='any', inplace=True)
            # df5t = df5t[df5t['rsi6'].notnull()]


            # 找出rsi最低点，设为买入价格的初始值
            min_rsi6 = df5t['rsi6'].min(axis=0)
            df5t.loc[df5t['rsi6'] == min_rsi6, 'signal'] = 1

            # 从signal == 1处开始遍历
            # 遍历DataFrame，查找K线相关的支撑和形态
            from_index = df5t.loc[df5t['signal'] == 1].index
            while True:
                print(df5t.loc[from_index])
                exit()

            print(from_index + 2)
            exit()




        # 做多信号
        lps.boll_upward_through(df=df)

        # 做多平仓
        lss.boll_downward_through(df=df)

        print(df)
        exit()

    @classmethod
    def get_data(cls, instrument_id, as_df=True, start_time=''):
        # result = cls.get_data_from_api(instrument_id, as_df=as_df)
        # result = cls.get_spot_from_mongo(instrument_id, as_df=as_df)

        # 历史数据测试
        # 数据起始时间：2020-01-05 13:49:00 -> 1578203340

        # 默认起始时间
        if not bool(start_time):
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


