# encoding=utf-8

import talib as ta


class MacdIndicator:
    @classmethod
    def get_value(cls, df, fastperiod=12, slowperiod=26, signalperiod=9):
        """
        计算MACD指标
        :param df:
        :param fastperiod:
        :param slowperiod:
        :param signalperiod:
        :return:
        """
        df['dif'], df['dea'], df['macd_bar'] = ta.MACD(df['close'], fastperiod=fastperiod, slowperiod=slowperiod, signalperiod=signalperiod)

