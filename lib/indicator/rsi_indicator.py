# encoding=utf-8

import talib as ta


class RsiIndicator:
    @classmethod
    def get_value(cls, df, rsi_name):
        """
        计算rsi线指标
        :param df:
        :param rsi_name:
        :return:
        """
        rsi_num = int(rsi_name.replace('rsi', ''))
        if rsi_num <= 0:
            return
        df[rsi_name] = ta.RSI(df['close'], timeperiod=rsi_num)

