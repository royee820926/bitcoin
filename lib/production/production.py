# encoding=utf-8

from lib.api.okex.swap_api import SwapApi
import pandas as pd
from config.swap_coin import swap_coin_type
from lib.strategy.long_position import LongPositionStrategy as lps

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
        # 获取当前数据
        instrument_id = 'BTC-USD-SWAP'
        result = SwapApi.get_kline_more(instrument_id)
        df = pd.DataFrame(result)

        # 计算指标


        # 找出做多信号
        lps.seek_one_signal(df)



