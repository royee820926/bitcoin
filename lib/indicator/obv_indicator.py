# encoding=utf-8
# 能量潮

import talib as ta


class ObvIndicator:
    @classmethod
    def get_value(cls, df):
        """
        获取能量潮指标（和okex有出入）
        :return:
        """
        df['obv'] = ta.OBV(df['close'], df['volume'])

