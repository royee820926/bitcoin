# encoding=utf-8

class BollIndicator:
    @classmethod
    def get_value(cls, df):
        """
        计算布林带
        :param df:
        :return:
        """
        n = 20  # 中轨n根K线的移动平均线
        m = 2  # 系数

        # 计算中轨
        df['boll_median'] = df['close'].rolling(n, min_periods=1).mean()

        # 计算标准差
        df['std'] = df['close'].rolling(n, min_periods=1).std(ddof=0)  # ddof 标准差自由度

        # 计算上轨
        df['boll_upper'] = df['boll_median'] + m * df['std']

        # 计算下轨
        df['boll_lower'] = df['boll_median'] - m * df['std']

