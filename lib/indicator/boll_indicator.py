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
        df['median'] = df['close'].rolling(n, min_periods=1).mean()
        # print(df.iloc[156: 180])
        # exit()
        # 计算标准差
        df['std'] = df['close'].rolling(n, min_periods=1).std(ddof=0)  # ddof 标准差自由度
        # 计算上轨
        df['upper'] = df['median'] + m * df['std']
        # 计算下轨
        df['lower'] = df['median'] - m * df['std']