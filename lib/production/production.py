# encoding=utf-8

from .data import Data
import pandas as pd
from config.swap_coin import swap_coin_type

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
        for instrument_id in swap_coin_type:
            print(instrument_id)
        exit()
        result = Data.get_current_data()
        df = pd.DataFrame(result)



