# encoding=utf-8

import time
import datetime


def get_dict(value, *param):
    """
    根据名字获取字典内容
    dict['aaa']['bbb']['ccc']
    调用: get_dict(dict, 'aaa', 'bbb', 'ccc')
    :param value:
    :param param:
    :return:
    """
    result = value
    for name in param:
        if name in result:
            result = result[name]
        else:
            return None
    return result


class TimeOption:
    @classmethod
    def string2datetime(cls, time_str, format_str, hours=0):
        """
        字符串转换为datetime
        :param time_str:
        :param format_str:
        :param hours:
        :return:
        """
        time_array = datetime.datetime.strptime(time_str, format_str)
        # 转换时区加减时间
        if hours != 0:
            time_array = time_array + datetime.timedelta(hours=hours)
        return time_array

    @classmethod
    def string2timestamp(cls, time_str, format_str, hours=0):
        """
        字符串转换为时间戳
        :param time_str:
        :param format_str:
        :param hours:
        :return:
        """
        time_array = cls.string2datetime(time_str, format_str, hours)
        return time.mktime(time_array.timetuple())

    @classmethod
    def datetime2timestamp(cls, time_array):
        """
        datetime转换为时间戳
        :param time_array:
        :return:
        """
        return time.mktime(time_array.timetuple())

    @classmethod
    def datetime2string(cls, date_time, format_str="%Y-%m-%d %H:%M:%S"):
        """
        datetime转字符串
        :param date_time:
        :param format_str:
        :return:
        """
        return time.strftime(format_str, date_time.timetuple())

    @classmethod
    def timestamp2string(cls, timestamp, format_str='%Y-%m-%d %H:%M:%S'):
        """
        时间戳转字符串
        :param timestamp:
        :param format_str:
        :return:
        """
        return time.strftime(format_str, cls.timestamp2datetime(timestamp))

    @classmethod
    def timestamp2datetime(cls, timestamp):
        """
        时间戳转datetime
        :param timestamp:
        :return:
        """
        return time.localtime(timestamp)

    @classmethod
    def set_datetime(cls, time_array, **params):
        """
        设置datetime
        :param time_array:
        :param params:
        :return:
        """
        for key, val in params.items():
            if key == 'second':
                time_array = time_array.replace(second=val)
        return time_array

class FundCalculator:
    """
    资金计算
    """
    __leverage_charge_rate = 0.0005

    @classmethod
    def long_leverage_income(cls, in_price, out_price, fund, leverage_rate):
        """
        做多杠杆收益
        :param in_price: 买入价格
        :param out_price: 卖出价格
        :param fund: 本金资金
        :param leverage_rate: 杠杆倍数
        :return:
        """
        total_fund = fund * leverage_rate
        repayment  = total_fund - fund
        # 上涨后的总资金
        final_fund = total_fund * (1 - cls.__leverage_charge_rate) / in_price * out_price * (1 - cls.__leverage_charge_rate)
        result = final_fund - repayment - fund
        return result

    @classmethod
    def short_leverage_income(cls, in_price, out_price, fund, leverage_rate):
        """
        做空杠杆收益
        :param in_price:
        :param out_price:
        :param fund:
        :param leverage_rate:
        :return:
        """
        total_fund = fund * leverage_rate
        # 归还数量
        repayment_number = total_fund / in_price
        repayment = out_price * repayment_number * (1 + cls.__leverage_charge_rate)
        result = total_fund - repayment - fund
        return result


