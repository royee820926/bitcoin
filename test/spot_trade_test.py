# encoding=utf-8

from .input_parameter import InputParameter


class SpotTradeTest:
    """
    现货交易资金曲线测试
    """
    # 更新间隔时间（秒）
    _update_interval = 86400

    @classmethod
    def money_curve(cls, df, capital=1000):
        """
        计算资金曲线
        :param df:
        :param capital: 资金（默认1000）
        :return:
        """
        # 更新现货交易参数
        InputParameter.update_spot_param(cls._update_interval)
        # 合并交易信号
        df['signal'] = df[['signal_lp', 'signal_ls']].sum(axis=1, min_count=1, skipna=True)

        print(df[['candle_begin_time', 'close', 'rsi6', 'signal_lp', 'signal_ls', 'signal']])
        exit()
        # 去除空值信号
        temp = df[df['signal'].notnull()]


        print(temp[['candle_begin_time', 'close', 'rsi6', 'signal_lp', 'signal_ls', 'signal']])
        exit()
