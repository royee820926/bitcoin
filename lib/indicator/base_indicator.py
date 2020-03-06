# encoding=utf-8

class BaseIndicator:
    """
    基础指标：
    涨幅，振幅...
    """

    @classmethod
    def increase(cls, df, interval=1):
        """
        涨幅
        :param df: 依赖值: open
        :param interval:
        :return:
        """
        df['increase'] = (df['open'] - df['open'].shift(interval)) / df['open'].shift(interval) * 100

    @classmethod
    def amplitude(cls, df):
        """
        振幅 = (当天的最高价格 - 最低价格） / 昨天收盘价格 * 100%
        :param df:
        :return:
        """
        pass
        # df['amplitude']
