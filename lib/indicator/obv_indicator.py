# encoding=utf-8
# 能量潮

class ObvIndicator:
    @classmethod
    def get_value(cls, df):
        """
        获取能量潮指标
        :return:
        """
        m = 30
        df['obv_va'] = df['volume'] if df['close'] > df['close'].shift(1) else (-df['volume'])
        # df['obv']


