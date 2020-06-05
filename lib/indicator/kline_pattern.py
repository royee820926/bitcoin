# encoding=utf-8

import talib as ta


class KlinePattern:
    @classmethod
    def hammer(cls, df):
        """
        锤子线
        :param df:
        :return:
        """
        return ta.CDLHAMMER(df['open'], df['high'], df['low'], df['close'])

    @classmethod
    def crows2(cls, df):
        """
        两只乌鸦
        :param df:
        :return:
        """
        return ta.CDL2CROWS(df['open'], df['high'], df['low'], df['close'])

    @classmethod
    def black_crows3(cls, df):
        """
        三只乌鸦
        :param df:
        :return:
        """
        return ta.CDL3BLACKCROWS(df['open'], df['high'], df['low'], df['close'])

    @classmethod
    def inside3(cls, df):
        """
        三内部上涨和下跌
        :param df:
        :return:
        """
        return ta.CDL3INSIDE(df['open'], df['high'], df['low'], df['close'])

    @classmethod
    def line_strike3(cls, df):
        """
        三线打击
        :param df:
        :return:
        """
        return ta.CDL3LINESTRIKE(df['open'], df['high'], df['low'], df['close'])

    @classmethod
    def out_side(cls, df):
        """
        三外部上涨和下跌
        :param df:
        :return:
        """
        return ta.CDL3OUTSIDE(df['open'], df['high'], df['low'], df['close'])

    @classmethod
    def stars_in_south(cls, df):
        """
        南方三星
        :param df:
        :return:
        """
        return ta.CDL3STARSINSOUTH(df['open'], df['high'], df['low'], df['close'])

    @classmethod
    def white_soldiers(cls, df):
        """
        三白兵
        :param df:
        :return:
        """
        return ta.CDL3WHITESOLDIERS(df['open'], df['high'], df['low'], df['close'])
