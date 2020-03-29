# encoding=utf-8
# 能量潮

import talib as ta


class ObvIndicator:
    @classmethod
    def get_value(cls, df):
        """
        获取能量潮指标
        :return:
        """
        # m = 30
        # df.loc[df['close'] > df['close'].shift(1), 'obv_va'] = df['volume']
        # df.loc[df['close'] < df['close'].shift(1), 'obv_va'] = -df['volume']
        # df['obvta'] = ta.OBV(df['close'], df['volume'])


