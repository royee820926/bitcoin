# encoding=utf-8

from lib.api.okex.swap_api import SwapApi
import pandas as pd
from lib.pandas_module import PandasModule
from config.swap_coin import swap_coin_type
from lib.strategy.long_position import LongPositionStrategy as lps
from lib.strategy.long_selling import LongSellingStrategy as lss

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
        instrument_id = 'BTC-USD-SWAP'
        result = SwapApi.get_kline_more(instrument_id)
        df = pd.DataFrame(result)
        df['candle_begin_time'] = pd.to_datetime(df['candle_begin_time'], format='%Y-%m-%d %H:%M:%S')

        # 重采样
        kline_rule = 5
        df = PandasModule.resample(df=df, kline_rule=kline_rule)

        # 计算指标

        # 做多信号
        lps.boll_upward_through(df=df)

        # 做多平仓
        lss.boll_downward_through(df=df)

        print(df)
        exit()

    @classmethod
    def append_data_frame(cls, df):
        """
        追加Dataframe数据
        :param df:
        :return:
        """
        pass

