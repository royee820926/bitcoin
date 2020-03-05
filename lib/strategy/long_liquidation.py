# encoding=utf-8


class LongLiquidationStrategy:
    """
    做多平仓
    """
    # 长上影线的比率（即将下行）
    _long_top_rate = 2
    # rsi上限阈值
    _rsi_upper_limit = 70
    # 做多平仓信号标志
    _signal = 1

    @classmethod
    def long_top_line(cls, df):
        """
        上影线
        :param df: 依赖值: macd_bar, ma60, close, rsi6
        :return:
        """
        # # 长上影线
        # kline_conf = (df['high'] - df['close']) / (df['close'] - df['open']) > cls._long_top_rate
        # 收盘价处于MA60均线上方
        close_conf = df['close'] > df['ma60']
        # rsi6 超卖
        rsi_conf = df['rsi6'] > cls._rsi_upper_limit
        df.loc[close_conf & rsi_conf, 'signal_ls'] = cls._signal



