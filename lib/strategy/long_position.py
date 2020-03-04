# encoding=utf-8


class LongPositionStrategy:
    """
    开仓做多
    """

    # macd粘合最大值
    _max_macd_overlap = 0
    # macd粘合最小值
    _min_macd_overlap = -2.5
    # rsi下限阈值
    _rsi_lower_limit = 30
    # 做多时，macd柱线的起始的最大值
    _macd_start_max = -4
    # 做多信号标志
    _signal = 2

    @classmethod
    def macd_overlap(cls, df):
        """
        dif、dea在接近0轴的下方粘合
        rsi小于下限值
        :param df: 依赖值: dif, dea, rsi6
        :return:
        """
        # 判断dif、dea粘合
        dif_conf = (df['dif'] < cls._max_macd_overlap) & (df['dif'] > cls._min_macd_overlap)
        dea_conf = (df['dea'] < cls._max_macd_overlap) & (df['dea'] > cls._min_macd_overlap)
        # 判断rsi小于下限值
        rsi_conf = (df['rsi6'] < cls._rsi_lower_limit) | \
                   (df['rsi6'].shift(1) < cls._rsi_lower_limit) | \
                   (df['rsi6'].shift(2) < cls._rsi_lower_limit)
        df.loc[dif_conf & dea_conf & rsi_conf, 'signal_up'] = cls._signal

    @classmethod
    def macd_multi_bar(cls, df, before_number=3):
        """
        macd多柱线一致减弱后突然增强
        :param df: 依赖值: macd_bar, ma60, close
        :param before_number: 需要判断前面的n个柱线
        :return:
        """
        # macd柱线小于0，并且大于前面的柱线；收盘价小于MA60均线
        macd_conf = (df['macd_bar'] < 0) & (df['macd_bar'] > df['macd_bar'].shift(1)) & (df['close'] < df['ma60'])
        if before_number > 0:
            for index in range(before_number):
                # 判断前面的柱线
                macd_conf = macd_conf & (df['macd_bar'].shift(index + 1) < cls._macd_start_max)
        df.loc[macd_conf, 'signal_up'] = cls._signal

