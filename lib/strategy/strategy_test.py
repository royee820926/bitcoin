# encoding=utf-8

from lib.strategy.long_liquidation import LongLiquidationStrategy as lls


class StrategyTest:
    """
    策略统计测试
    """

    @classmethod
    def rsi_increase_test(cls, df, base_index):
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
        print(df.iloc[base_index]['candle_begin_time'])
        print('#' * 40)

        while True:
            curr_index += 1
            max_rsi6 = 0
            print(df.iloc[curr_index]['candle_begin_time'])
            try:
                # 计算涨幅
                curr_close = df.iloc[curr_index]['close']
                increase = (curr_close - base_close) / base_close * 100
                rsi6 = df.iloc[curr_index]['rsi6']
                prev_rsi6 = df.iloc[curr_index - 1]['rsi6']
                signal_lp = df.iloc[curr_index]['signal_lp']
                # 最大rsi
                if rsi6 > max_rsi6:
                    max_rsi6 = rsi6
                    max_time = df.iloc[curr_index]['candle_begin_time']

                # 到达下一个做多信号
                if signal_lp == 1:
                    # 避免两个做多信号相隔太近
                    if curr_index - base_index > 3:

                        print('stop test')
                        print(max_time)
                        print(max_rsi6)
                        exit()

                # 计算平仓，如果rsi6的跌幅超过15% 或 rsi6大于rsi_upper_limit
                rsi6_increase = (rsi6 - prev_rsi6) / prev_rsi6 * 100

                # if prev_rsi6 > lls.get_rsi_upper_limit() or (prev_rsi6 > 50 and rsi6_increase < -10):
                # 前一个rsi6大于50，前一个rsi6大于当前rsi6
                if prev_rsi6 > 60 and prev_rsi6 > rsi6:
                    print(rsi6_increase)
                    print(prev_rsi6, rsi6)
                    print(df.iloc[curr_index]['candle_begin_time'])
                    print('current_close: %s' % curr_close)
                    print('涨幅: %s' % increase)
                    exit()

            except IndexError:
                # curr_index 超出范围
                print('current index is out of range')
                exit()

