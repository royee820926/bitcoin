# encoding=utf-8

import talib as ta


class EmaIndicator:
    @classmethod
    def get_value(cls, df, ema_name):
        """
        计算指数移动平均线指标
        :param df:
        :param ema_name:
        :return:
        """
        ema_num = int(ema_name.replace('ema', ''))
        if ema_num > 0:
            df[ema_name] = ta.EMA(df['close'], timeperiod=ema_num)
        return

