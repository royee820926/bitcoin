# encoding=utf-8

from lib.strategy.long_position import LongPositionStrategy as lps


class LongLiquidationStrategy:
    """
    做多平仓
    """
    # 长上影线的比率（即将下行）
    _long_top_rate = 2
    # rsi上限阈值
    _rsi_upper_limit = 75
    # 做多平仓信号标志
    _signal = 1
    _signal_key = 'signal_ls'

    @classmethod
    def get_rsi_upper_limit(cls):
        return cls._rsi_upper_limit

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

    @classmethod
    def find_rsi_top(cls, df):
        """
        从DataFrame的指定开始和结束位置查询平仓信号
        :param df:
        :return:
        """
        # 查询做多信号为1的记录
        long_signal = df[df[lps.get_signal_key()] == 1]

        # 遍历做多信号，逐个生成后续的平仓信号
        for item in long_signal.iterrows():
            index = item[0]
            # print(index)
            # exit()
            cls.one_rsi_top(df, index)

    @classmethod
    def one_rsi_top(cls, df, base_index):
        """
        rsi涨幅和K线涨幅，测试涨跌力度
        基于signal_lp做多信号，向后统计
        :param df: 依赖值: rsi, signal_lp
        :param base_index:
        :return:
        """
        base_item = df.iloc[base_index]
        base_close = base_item['close']
        curr_index = base_index
        # print(df.iloc[base_index]['candle_begin_time'])
        # print('#' * 40)

        while True:
            curr_index += 1
            max_rsi6 = 0
            # print(df.iloc[curr_index]['candle_begin_time'])
            try:
                # 计算涨幅
                curr_close = df.iloc[curr_index]['close']
                increase = (curr_close - base_close) / base_close * 100

                curr_time = df.iloc[curr_index]['candle_begin_time']
                rsi6 = df.iloc[curr_index]['rsi6']
                prev_rsi6 = df.iloc[curr_index - 1]['rsi6']
                signal_lp = df.iloc[curr_index]['signal_lp']

                # 最大rsi（测试）
                # if rsi6 > max_rsi6:
                #     max_rsi6 = rsi6
                #     max_time = df.iloc[curr_index]['candle_begin_time']

                # 到达下一个做多信号
                if signal_lp == 1:
                    # 避免两个做多信号相隔太近
                    if curr_index - base_index > 5:
                        break
                        # print('stop test')
                        # print(max_time)
                        # print(max_rsi6)
                        # exit()

                # 计算平仓，如果rsi6的跌幅超过15% 或 rsi6大于rsi_upper_limit
                rsi6_increase = (rsi6 - prev_rsi6) / prev_rsi6 * 100

                # 前一个rsi6大于50，前一个rsi6大于当前rsi6
                if prev_rsi6 > 60 and prev_rsi6 > rsi6:
                    # 设置平仓信号
                    df.loc[df['candle_begin_time'] == curr_time, cls._signal_key] = cls._signal
                    break

                    # print(rsi6_increase)
                    # print(prev_rsi6, rsi6)
                    # print(df.iloc[curr_index]['candle_begin_time'])
                    # print('current_close: %s' % curr_close)
                    # print('涨幅: %s' % increase)
                    # exit()

            except IndexError:
                # curr_index 超出范围
                break



