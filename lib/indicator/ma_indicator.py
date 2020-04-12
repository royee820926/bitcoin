# encoding=utf-8

class MaIndicator:
    @classmethod
    def get_value(cls, df, ma_name):
        """
        计算移动平均线指标
        :param df:
        :param ma_name:
        :return:
        """
        ma_num = int(ma_name.replace('ma', ''))
        if ma_num <= 0:
            return
        df[ma_name] = df['close'].rolling(ma_num, min_periods=1).mean()


