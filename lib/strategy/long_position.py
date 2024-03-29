# encoding=utf-8

from lib.indicator.base_indicator import BaseIndicator


class LongPositionStrategy:
    """
    开仓做多
    """

    # macd粘合最大值
    _max_macd_overlap = 0
    # macd粘合最小值
    _min_macd_overlap = -4
    # rsi下限阈值
    _rsi_lower_limit = 25
    # 做多时，macd柱线的起始的最大值
    _macd_start_max = -4
    # 做多信号标志
    _signal = 1
    _signal_key = 'signal_lp'

    @classmethod
    def get_signal_key(cls):
        """
        获取信号的键名
        :return:
        """
        return cls._signal_key

    @classmethod
    def macd_overlap(cls, df):
        """
        dif、dea在接近0轴的下方粘合
        rsi小于下限值
        :param df: 依赖值: dif, dea, rsi6
        :return:
        """
        # 计算需要的指标
        BaseIndicator.rely_on_indicator(df, ['dif', 'dea', 'macd_bar'])

        # 判断dif、dea粘合
        dif_conf = (df['dif'] < cls._max_macd_overlap) & (df['dif'] > cls._min_macd_overlap)
        dea_conf = (df['dea'] < cls._max_macd_overlap) & (df['dea'] > cls._min_macd_overlap)
        # 判断rsi小于下限值
        rsi_conf = (df['rsi6'] < cls._rsi_lower_limit) | \
                   (df['rsi6'].shift(1) < cls._rsi_lower_limit) | \
                   (df['rsi6'].shift(2) < cls._rsi_lower_limit)
        df.loc[dif_conf & dea_conf & rsi_conf, cls._signal_key] = cls._signal
        return True

    @classmethod
    def macd_multi_bar(cls, df, before_number=3):
        """
        macd多柱线一致减弱后突然增强
        :param df: 依赖值: macd_bar, ma60, close
        :param before_number: 需要判断前面的n个柱线
        :return:
        """
        # 计算需要的指标
        BaseIndicator.rely_on_indicator(df, ['macd_bar', 'ma60'])

        # macd柱线小于0，并且大于前面的柱线；收盘价小于MA60均线
        macd_conf = (df['macd_bar'] < 0) & (df['macd_bar'] > df['macd_bar'].shift(1)) & (df['close'] < df['ma60'])
        if before_number > 0:
            for index in range(before_number):
                # 判断前面的柱线
                macd_conf = macd_conf & (df['macd_bar'].shift(index + 1) < cls._macd_start_max)
        df.loc[macd_conf, cls._signal_key] = cls._signal
        return True

    @classmethod
    def lower_rsi_next(cls, df):
        """
        rsi低点
        :param df: 依赖值: rsi6, macd_bar
        :return:
        """
        # 计算需要的指标
        BaseIndicator.rely_on_indicator(df, ['rsi6'])

        # 前一条rsi指标低于rsi_lower_limit，rsi6指标高于前一条rsi指标
        rsi_conf = (df['rsi6'].shift(1) < cls._rsi_lower_limit) & (df['rsi6'] > df['rsi6'].shift(1))
        # macd柱线
        # macd_conf = df['macd_bar'] > cls._min_macd_overlap

        # df.loc[rsi_conf & macd_conf, cls._signal_key] = cls._signal
        df.loc[rsi_conf, cls._signal_key] = cls._signal
        return True

    @classmethod
    def macd_upward_through(cls, df):
        """
        macd线上穿越0轴，由负变正
        :param df: 依赖值: dif, dea, macd_bar
        :return:
        """
        # 计算需要的指标
        BaseIndicator.rely_on_indicator(df, ['dif', 'dea', 'macd_bar'])

        macd_conf  = (df['macd_bar'] > 0) & (df['macd_bar'].shift(1) < 0) & (df['dea'].shift(1) < 0)
        dif_conf   = (df['dif'] > df['dea']) & (df['dif'].shift(1) < df['dea'].shift(1))
        df.loc[macd_conf & dif_conf, cls._signal_key] = cls._signal
        return True

    @classmethod
    def boll_upward_through(cls, df):
        """
        布林带上穿下轨
        :param df:
        :return:
        """
        # 计算需要的指标
        BaseIndicator.rely_on_indicator(df, ['boll_upper'])

        boll_conf = (df['close'] > df['boll_upper']) & (df['close'].shift(1) < df['boll_upper'].shift(1))
        df.loc[boll_conf, cls._signal_key] = cls._signal
        return True

    @classmethod
    def seek_one_signal(cls, df):
        """
        遍历找出一个做多信号
        :param df:
        :return:
        """
        df_num = len(df)

        print(len(df))
        exit()
