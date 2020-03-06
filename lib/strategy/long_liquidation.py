# encoding=utf-8


class LongLiquidationStrategy:
    """
    做多平仓
    """
    # 长上影线的比率（即将下行）
    _long_top_rate = 2
    # rsi上限阈值
    _rsi_upper_limit = 80
    # 做多平仓信号标志
    _signal = 1
    _signal_key = 'signal_ls'

    @classmethod
    def long_top_line(cls, df):
        """
        上影线
        :param df: 依赖值: macd_bar, ma60, close, rsi6
        :return:
        """
        # 收盘价处于MA60均线上方
        close_conf = df['close'] > df['ma60']
        # rsi6 超卖
        rsi_conf = df['rsi6'] > cls._rsi_upper_limit
        df.loc[close_conf & rsi_conf, cls._signal_key] = cls._signal
        return True

    @classmethod
    def macd_multi_bar(cls, df, inc_num=3):
        """
        macd多柱线向上增强后减弱
        :param df: 依赖值: macd_bar
        :param inc_num:
        :return:
        """
        if inc_num <= 0:
            return False
        low_conf = df['macd_bar'] < df['macd_bar'].shift(1)
        inc_conf = False
        for index in range(inc_num):
            inc_conf = inc_conf & (df['macd_bar'].shift(index + 1) > df['macd_bar'].shift(index + 2))
        df.loc[low_conf & inc_conf, cls._signal_key] = cls._signal
        return True

